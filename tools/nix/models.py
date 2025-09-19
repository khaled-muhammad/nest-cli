import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PackageMaintainer:
    name: str
    github: str
    email: str

@dataclass
class PackageTeam:
    members: List[PackageMaintainer]
    scope: str
    short_name: str
    github_teams: List[str]

@dataclass
class PackageLicense:
    url: Optional[str]
    full_name: str

@dataclass
class NixPackage:
    attr_name: str
    attr_set: str
    pname: str
    pversion: str
    platforms: List[str]
    outputs: List[str]
    default_output: str
    programs: List[str]
    main_program: Optional[str]
    licenses: List[PackageLicense]
    maintainers: List[PackageMaintainer]
    teams: List[PackageTeam]
    description: Optional[str]
    long_description: Optional[str]
    homepage: List[str]
    position: str
    system: str
    hydra: Optional[str]
    score: float

@dataclass
class AggregationBucket:
    key: str
    doc_count: int

@dataclass
class Aggregation:
    doc_count_error_upper_bound: int
    sum_other_doc_count: int
    buckets: List[AggregationBucket]

@dataclass
class SearchResponse:
    took: int
    timed_out: bool
    total_hits: int
    max_score: Optional[float]
    packages: List[NixPackage]
    aggregations: Optional[Dict[str, Any]]

class NixOSSearchParser:
    """Parser for NixOS package search API responses"""
    
    @staticmethod
    def parse_maintainer(maintainer_data: Dict) -> PackageMaintainer:
        """Parse a single maintainer object"""
        return PackageMaintainer(
            name=maintainer_data.get("name", ""),
            github=maintainer_data.get("github", ""),
            email=maintainer_data.get("email", "")
        )
    
    @staticmethod
    def parse_team(team_data: Dict) -> PackageTeam:
        """Parse a single team object"""
        members = [
            NixOSSearchParser.parse_maintainer(member) 
            for member in team_data.get("members", [])
        ]
        return PackageTeam(
            members=members,
            scope=team_data.get("scope", ""),
            short_name=team_data.get("shortName", ""),
            github_teams=team_data.get("githubTeams", [])
        )
    
    @staticmethod
    def parse_license(license_data: Dict) -> PackageLicense:
        """Parse a single license object"""
        return PackageLicense(
            url=license_data.get("url"),
            full_name=license_data.get("fullName", "")
        )
    
    @staticmethod
    def parse_package(hit: Dict) -> NixPackage:
        """Parse a single package from search hit"""
        source = hit["_source"]
        
        # Parse maintainers
        maintainers = [
            NixOSSearchParser.parse_maintainer(m) 
            for m in source.get("package_maintainers", [])
        ]
        
        # Parse teams
        teams = [
            NixOSSearchParser.parse_team(t) 
            for t in source.get("package_teams", [])
        ]
        
        # Parse licenses
        licenses = [
            NixOSSearchParser.parse_license(l) 
            for l in source.get("package_license", [])
        ]
        
        return NixPackage(
            attr_name=source.get("package_attr_name", ""),
            attr_set=source.get("package_attr_set", ""),
            pname=source.get("package_pname", ""),
            pversion=source.get("package_pversion", ""),
            platforms=source.get("package_platforms", []),
            outputs=source.get("package_outputs", []),
            default_output=source.get("package_default_output", ""),
            programs=source.get("package_programs", []),
            main_program=source.get("package_mainProgram"),
            licenses=licenses,
            maintainers=maintainers,
            teams=teams,
            description=source.get("package_description"),
            long_description=source.get("package_longDescription"),
            homepage=source.get("package_homepage", []),
            position=source.get("package_position", ""),
            system=source.get("package_system", ""),
            hydra=source.get("package_hydra"),
            score=hit.get("_score", 0.0)
        )
    
    @staticmethod
    def parse_aggregation_buckets(buckets_data: List[Dict]) -> List[AggregationBucket]:
        """Parse aggregation buckets"""
        return [
            AggregationBucket(
                key=bucket["key"],
                doc_count=bucket["doc_count"]
            )
            for bucket in buckets_data
        ]
    
    @staticmethod
    def parse_aggregation(agg_data: Dict) -> Aggregation:
        """Parse a single aggregation"""
        return Aggregation(
            doc_count_error_upper_bound=agg_data.get("doc_count_error_upper_bound", 0),
            sum_other_doc_count=agg_data.get("sum_other_doc_count", 0),
            buckets=NixOSSearchParser.parse_aggregation_buckets(agg_data.get("buckets", []))
        )
    
    @classmethod
    def build_search_query(cls, query: str, from_idx: int = 0, size: int = 50) -> Dict[str, Any]:
        """Build the search query payload"""
        return {
            "from": from_idx,
            "size": size,
            "sort": [
                {"_score": "desc", "package_attr_name": "desc", "package_pversion": "desc"}
            ],
            "aggs": {
                "package_attr_set": {"terms": {"field": "package_attr_set", "size": 20}},
                "package_license_set": {"terms": {"field": "package_license_set", "size": 20}},
                "package_maintainers_set": {"terms": {"field": "package_maintainers_set", "size": 20}},
                "package_teams_set": {"terms": {"field": "package_teams_set", "size": 20}},
                "package_platforms": {"terms": {"field": "package_platforms", "size": 20}},
                "all": {
                    "global": {},
                    "aggregations": {
                        "package_attr_set": {"terms": {"field": "package_attr_set", "size": 20}},
                        "package_license_set": {"terms": {"field": "package_license_set", "size": 20}},
                        "package_maintainers_set": {"terms": {"field": "package_maintainers_set", "size": 20}},
                        "package_teams_set": {"terms": {"field": "package_teams_set", "size": 20}},
                        "package_platforms": {"terms": {"field": "package_platforms", "size": 20}}
                    }
                }
            },
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"type": {"value": "package", "_name": "filter_packages"}}},
                        {
                            "bool": {
                                "must": [
                                    {"bool": {"should": []}},
                                    {"bool": {"should": []}},
                                    {"bool": {"should": []}},
                                    {"bool": {"should": []}},
                                    {"bool": {"should": []}}
                                ]
                            }
                        }
                    ],
                    "must_not": [],
                    "must": [
                        {
                            "dis_max": {
                                "tie_breaker": 0.7,
                                "queries": [
                                    {
                                        "multi_match": {
                                            "type": "cross_fields",
                                            "query": query,
                                            "analyzer": "whitespace",
                                            "auto_generate_synonyms_phrase_query": False,
                                            "operator": "and",
                                            "_name": f"multi_match_{query.replace(' ', '_')}",
                                            "fields": [
                                                "package_attr_name^9",
                                                "package_attr_name.*^5.3999999999999995",
                                                "package_programs^9",
                                                "package_programs.*^5.3999999999999995",
                                                "package_pname^6",
                                                "package_pname.*^3.5999999999999996",
                                                "package_description^1.3",
                                                "package_description.*^0.78",
                                                "package_longDescription^1",
                                                "package_longDescription.*^0.6",
                                                "flake_name^0.5",
                                                "flake_name.*^0.3"
                                            ]
                                        }
                                    },
                                    {
                                        "wildcard": {
                                            "package_attr_name": {
                                                "value": f"*{query}*",
                                                "case_insensitive": True
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

    @staticmethod
    def parse_response(data) -> SearchResponse:
        """Parse the complete search response"""
        packages = []
        hits = data.get("hits", {}).get("hits", [])
        for hit in hits:
            try:
                packages.append(NixOSSearchParser.parse_package(hit))
            except Exception as e:
                print(f"Error parsing package {hit.get('_id', 'unknown')}: {e}")
                continue
        
        # Parse aggregations if present
        aggregations = {}
        if "aggregations" in data:
            for agg_name, agg_data in data["aggregations"].items():
                try:
                    if isinstance(agg_data, dict) and "buckets" in agg_data:
                        aggregations[agg_name] = NixOSSearchParser.parse_aggregation(agg_data)
                    else:
                        # Handle nested aggregations (like the structure in your data)
                        aggregations[agg_name] = agg_data
                except Exception as e:
                    print(f"Error parsing aggregation {agg_name}: {e}")
                    aggregations[agg_name] = agg_data
        
        return SearchResponse(
            took=data.get("took", 0),
            timed_out=data.get("timed_out", False),
            total_hits=data.get("hits", {}).get("total", {}).get("value", 0),
            max_score=data.get("hits", {}).get("max_score"),
            packages=packages,
            aggregations=aggregations if aggregations else None
        )