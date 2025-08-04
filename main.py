import air
from air_markdown import Markdown
from svgs import Air1ColorLogo, Air3ColorLogo
from fastapi import HTTPException
from fastapi import FastAPI
from pathlib import Path

app = air.Air()
api = FastAPI()

app.mount("/static", air.StaticFiles(directory="static"), name="static")


def nav():
    return air.Nav(
        air.A("Home", href="/"),
        air.A("Usage Policy", href="/usage-policy"),
    )


def footer():
    return air.Footer(
        air.P(
            "© 2025 Feldroy. All rights reserved. This website is powered by ",
            air.A("Air", href="https://air.feldroy.com"),
            " 🌬️ View the source code on ",
            air.A("GitHub", href="https://github.com/feldroy/air-svgs")
        )
    )


@app.page
def index():
    return air.layouts.picocss(
        nav(),
        air.Title("Air SVGs"),
        air.H1("Air SVGs"),
        air.P("This page contains the Air logo (and more soon) in SVG format."),
        
        air.H2("1-Color"),
        air.Img(src="/static/air-deep-sky-blue.svg", alt="Air Logo in 1 color (Deep Sky Blue)", width=200, height=200),
        air.Div(
            air.A(
                "Download SVG (Deep Sky Blue)",
                href="/static/air-deep-sky-blue.svg",
                download=True,
            ),
            air.Span(" | "),
            air.A(
                "Download SVG (Neon)",
                href="/static/air-neon.svg",
                download=True,
            ),
        ),

        air.H2("3-Color"),
        air.Img(src="/static/air-3color.svg", alt="Air Logo in 3 colors", width=200, height=200),

        air.Div(
            air.A(
                "Download SVG",
                href="/static/air-3color.svg",
                download=True,
            ),
        ),

        air.H2("1-color logo rendered from an Air Tag"),
        Air1ColorLogo(),

        air.H2("3-color logo rendered from an Air Tag"),
        Air3ColorLogo(),

        air.H2("Need Other SVGs?"),
        air.P(
            air.Span("If you need other variations for a particular use case you have in mind: "),
            air.A("Open an issue with details", href="https://github.com/feldroy/air-svgs/issues/new"),
            air.Span(" and we'll see what we can do.")
        ),
        footer()
    )


def layout(request: air.Request, *content):
    if not isinstance(request, air.Request):
        raise Exception('First arg of layout needs to be an air.Request')
    return air.layouts.picocss(
        nav(),
        *content,
        footer()
    )


@app.get('/{slug:path}')
def mdpage(request: air.Request, slug: str):
    path = Path(f"pages/{slug}.md")
    if path.exists():
        text = path.read_text()
        # TODO add fetching of page title from first H1 tag
        return layout(
            request, Markdown(text)
        )
    path = Path(f"pages/{slug}.py")
    if path.exists():
        module_name = f'pages.{slug.replace('/', '.')}'     
        mod = importlib.import_module(module_name)
        return layout(
            request, mod.render(request)
        )
    raise HTTPException(status_code=404)


if __name__ == "__main__":
    print("Run this with fastapi dev")
