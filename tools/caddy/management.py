from .models import CaddyFile, SiteBlock, Directive

def listSites():
    caddy = CaddyFile.parse('~/Caddyfile')
    # caddy = CaddyFile.parse('/home/khaled/nest-cli/CaddyfileTest')

    return caddy.sites

def addReverseProxy(site:SiteBlock, path, port):
    for directive in site.directives:
        if directive.name in ('handle', 'handle_path', 'reverse_proxy'):
            if len(directive.args) != 0 and directive.args[0] == path:
                raise ValueError("Path actually does exist in this site block!")
    
    site.add_directive(Directive("handle", [path], [
        Directive("reverse_proxy", [f":{port}"])
    ]))

    return site

def addStaticRoute(site:SiteBlock, route_path, path):
    for directive in site.directives:
        if directive.name in ('handle', 'handle_path', 'reverse_proxy'):
            if len(directive.args) != 0 and directive.args[0] == route_path:
                raise ValueError("Path actually does exist in this site block!")

    site.add_directive(Directive("handle_path", [route_path], [
        Directive("root", ["*", path]),
        Directive("file_server")
    ]))

    return site

def saveUpdatedSite(site:SiteBlock):
    caddy = CaddyFile.parse('~/Caddyfile')
    # caddy = CaddyFile.parse('/home/khaled/nest-cli/CaddyfileTest')

    caddy.sites[site.domain] = site

    caddy.save('~/Caddyfile')
    # caddy.save('/home/khaled/nest-cli/CaddyfileTest')

def deleteSite(site:SiteBlock):
    caddy = CaddyFile.parse('~/Caddyfile')
    # caddy = CaddyFile.parse('/home/khaled/nest-cli/CaddyfileTest')

    del caddy.sites[site.domain]

    caddy.save('~/Caddyfile')
    # caddy.save('/home/khaled/nest-cli/CaddyfileTest')