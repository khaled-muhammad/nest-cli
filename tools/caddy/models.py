import os
from pathlib import Path
from typing import List, Optional

class Directive:
    def __init__(self, name: str, args: Optional[List[str]] = None, subdirectives: Optional[List['Directive']] = None):
        self.name          = name
        self.args          = args or []
        self.subdirectives = subdirectives or []
    
    def add_arg(self, arg: str):
        self.args.append(arg)
    
    def add_subdirective(self, subdirective: 'Directive'):
        self.subdirectives.append(subdirective)
    
    def render(self, indent: int = 0) -> str:
        indent_str = ' ' * (indent * 4)
        args_str   = ' '.join(self.args)
        lines      = [f"{indent_str}{self.name} {args_str}"]

        if self.subdirectives:
            lines[0] += " {"
            for sub in self.subdirectives:
                lines.append(sub.render(indent + 1))
            lines.append(f"{indent_str}}}")

        return "\n".join(lines)

    def __str__(self):
        return f"{self.name} | {self.args} | {len(self.subdirectives)}"

class SiteBlock:
    def __init__(self, domain: str, directives, bind):
        self.domain     = domain
        self.directives = directives or []
        self.bind       = bind

    def add_directive(self, directive: Directive):
        self.directives.append(directive)

    def set_directives(self, directives: List[Directive]):
        self.directives = directives
    
    def render(self) -> str:
        lines = [f"http://{self.domain} {{"]

        if self.bind:
            lines.append(f"    bind {self.bind}")

        for directive in self.directives:
            rendered = directive.render(indent=1)
            lines.append(rendered)

        lines.append("}")
        return "\n".join(lines)

class CaddyFile:
    def __init__(self, admin: Optional[str] = None):
        self.admin       = admin
        self.sites       = {}

    def add_site(self, site: SiteBlock):
        self.sites[site.domain] = site
    
    def update_site(self, domain: str, bind: Optional[str] = None, directives: Optional[List[str]] = None):
        if domain not in self.sites:
            self.sites[domain] = SiteBlock(domain, directives or [], bind)
        else:
            site = self.sites[domain]
            if bind:
                site.bind = bind
            if directives:
                site.set_directives(directives)

    def render(self) -> str:
        output = []
        if self.admin:
            output.append(f"{{\n    admin {self.admin}\n}}\n")
        for site in self.sites.values():
            output.append(site.render())
            output.append("")
        return "\n".join(output).strip()

    def save(self, path: str | Path):
        Path(os.path.expanduser(path)).write_text(self.render(), encoding="utf-8")

    @staticmethod
    def parse(path) -> 'CaddyFile':
        with open(os.path.expanduser(path), 'r', encoding='utf-8') as file:
            lines = file.readlines()

        caddyfile = CaddyFile()
        current_site = None

        def parse_directives(lines: List[str], start_index: int = 0) -> (List[Directive], int):
            directives = []
            i = start_index
            while i < len(lines):
                line = lines[i].strip()
                if line == "}":
                    return directives, i
                if not line or line.startswith("#"):
                    i += 1
                    continue

                parts = line.split()
                name  = parts[0]
                args  = parts[1:]

                if args and args[-1] == "{":
                    args.pop()
                    subdirectives, new_index = parse_directives(lines, i + 1)
                    directives.append(Directive(name, args, subdirectives))
                    i = new_index + 1
                else:
                    directives.append(Directive(name, args))
                    i += 1
            return directives, i

        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue

            if line.strip().startswith("{"):
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("}"):
                    inner_line = lines[i].strip()
                    if inner_line.startswith("admin"):
                        parts = inner_line.split()
                        if len(parts) == 2:
                            caddyfile.admin = parts[1]
                        elif len(parts) == 1 and i + 1 < len(lines):
                            next_line = lines[i+1].strip()
                            caddyfile.admin = next_line
                            i += 1
                    i += 1
                continue

            if line.startswith("http://") or line.startswith("https://"):
                domain = line.split()[0].replace("http://", "").replace("https://", "")
                current_site = SiteBlock(domain, [], None)
                i += 1

                while i < len(lines):
                    inner_line = lines[i].strip()
                    if inner_line == "}":
                        caddyfile.add_site(current_site)
                        current_site = None
                        i += 1
                        break
                    if inner_line.startswith("bind"):
                        bind_parts = inner_line.split()
                        if len(bind_parts) == 2:
                            current_site.bind = bind_parts[1]
                        i += 1
                        continue

                    directives, new_index = parse_directives(lines, i)
                    for directive in directives:
                        current_site.add_directive(directive)
                    i = new_index
            else:
                i += 1
        return caddyfile

if __name__ == "__main__":
    # caddyfile = CaddyFile(admin="unix//home/khaled/caddy-admin.sock")

    # # --- khaled.hackclub.app ---
    # site1 = SiteBlock("khaled.hackclub.app", [], "unix/.khaled.hackclub.app.webserver.sock|777")
    # site1.add_directive(Directive("root", ["*", "/home/khaled/pub"]))
    # site1.add_directive(Directive("file_server", subdirectives=[
    #     Directive("hide", [".git", ".env"])
    # ]))
    # caddyfile.add_site(site1)

    # # --- sweetheart-mini.kozow.com ---
    # site2 = SiteBlock("sweetheart-mini.kozow.com", [], "unix/.khaled.hackclub.app.webserver.sock|777")
    # site2.add_directive(Directive("root", ["*", "/home/khaled/pub"]))
    # site2.add_directive(Directive("file_server", subdirectives=[
    #     Directive("hide", [".git", ".env"])
    # ]))
    # caddyfile.add_site(site2)

    # # --- moodle.khaled.hackclub.app ---
    # site3 = SiteBlock("moodle.khaled.hackclub.app", [], "unix/.khaled.hackclub.app.webserver.sock|777")
    # site3.add_directive(Directive("reverse_proxy", ["localhost:1456"]))
    # caddyfile.add_site(site3)

    # # --- hackclub-cdn.khaled.hackclub.app ---
    # site4 = SiteBlock("hackclub-cdn.khaled.hackclub.app", [], "unix//home/khaled/.hackclub-cdn.khaled.hackclub.app.webserver.sock|777")
    # site4.add_directive(Directive("handle_path", ["/assets/*"], [
    #     Directive("root", ["*", "/home/khaled/hackclub_cdn_backend/staticfiles"]),
    #     Directive("file_server")
    # ]))
    # site4.add_directive(Directive("reverse_proxy", [":45153"]))
    # caddyfile.add_site(site4)

    # # --- hd.khaled.hackclub.app ---
    # site5 = SiteBlock("hd.khaled.hackclub.app", [], "unix//home/khaled/.hd.khaled.hackclub.app.webserver.sock|777")
    # site5.add_directive(Directive("handle_path", ["/downloads/*"], [
    #     Directive("root", ["*", "/home/khaled/hackducky/binaries"]),
    #     Directive("file_server")
    # ]))
    # site5.add_directive(Directive("reverse_proxy", [":45521"]))
    # caddyfile.add_site(site5)

    # # --- move-itt.xyz ---
    # site6 = SiteBlock("move-itt.xyz", [], "unix//home/khaled/.move-itt.xyz.webserver.sock|777")
    # site6.add_directive(Directive("root", ["*", "/home/khaled/moveit/dist"]))
    # site6.add_directive(Directive("handle", ["/api/*"], [
    #     Directive("reverse_proxy", [":45631"])
    # ]))
    # site6.add_directive(Directive("handle", ["/ws/*"], [
    #     Directive("reverse_proxy", [":45631"])
    # ]))
    # site6.add_directive(Directive("handle", ["/admin/*"], [
    #     Directive("reverse_proxy", [":45631"])
    # ]))
    # site6.add_directive(Directive("handle_path", ["/static/*"], [
    #     Directive("root", ["*", "/home/khaled/moveit/moveit_backend/staticfiles/"]),
    #     Directive("file_server")
    # ]))
    # site6.add_directive(Directive("handle_path", ["/media/*"], [
    #     Directive("root", ["*", "/home/khaled/moveit/moveit_backend/media/"]),
    #     Directive("file_server")
    # ]))
    # site6.add_directive(Directive("handle", [], [
    #     Directive("try_files", ["{path}", "/index.html"]),
    #     Directive("file_server")
    # ]))
    # site6.add_directive(Directive("encode", ["gzip"]))
    # caddyfile.add_site(site6)

    # # --- airsynca.com ---
    # site7 = SiteBlock("airsynca.com", [], "unix//home/khaled/.airsynca.com.webserver.sock|777")
    # site7.add_directive(Directive("root", ["*", "/home/khaled/moveit/dist"]))
    # site7.add_directive(Directive("handle", ["/api/*"], [
    #     Directive("reverse_proxy", [":45631"])
    # ]))
    # site7.add_directive(Directive("handle", ["/ws/*"], [
    #     Directive("reverse_proxy", [":45631"])
    # ]))
    # site7.add_directive(Directive("handle", ["/admin/*"], [
    #     Directive("reverse_proxy", [":45631"])
    # ]))
    # site7.add_directive(Directive("handle_path", ["/static/*"], [
    #     Directive("root", ["*", "/home/khaled/moveit/moveit_backend/staticfiles/"]),
    #     Directive("file_server")
    # ]))
    # site7.add_directive(Directive("handle_path", ["/media/*"], [
    #     Directive("root", ["*", "/home/khaled/moveit/moveit_backend/media/"]),
    #     Directive("file_server")
    # ]))
    # site7.add_directive(Directive("handle", [], [
    #     Directive("try_files", ["{path}", "/index.html"]),
    #     Directive("file_server")
    # ]))
    # site7.add_directive(Directive("encode", ["gzip"]))
    # caddyfile.add_site(site7)

    caddyfile = CaddyFile.parse("~/Caddyfile")

    # Save
    caddyfile.save("CaddyfileTest")
