from jinja2 import Environment, FileSystemLoader, select_autoescape
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions
from pathlib import Path
import base64
import subprocess

module_path , _= __name__.rsplit(".", maxsplit=1)
module_path = Path(module_path.replace(".", "/"))
jinja = Environment(loader=FileSystemLoader(module_path / "resources"), autoescape=select_autoescape())

def render_feeds(config: dict[str, any], feeds:list[dict[str, any]]):
    template = jinja.get_template("main.html")
    data = template.render(
        sites=feeds
    )

    with open("render.html", "w") as fp:
        fp.write(data)

    path = Path("./render.html")
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(120)
    driver.implicitly_wait(20)
    driver.get(f'file://{path.absolute()}')

    print_options = PrintOptions()
    pdf = driver.print_page(print_options=print_options)
    path.unlink()

    if config['pdf_only']:
        with open("render.pdf", "wb") as fp:
            fp.write(base64.b64decode(pdf))
    else:
        # send pdf to printer
        with open("render.pdf", "wb") as fp:
            fp.write(base64.b64decode(pdf))

        subprocess.run(f"pdftops render.pdf -| lp -d {config['fax_printer']}", shell=True)
        Path("render.pdf").unlink()

    driver.close()
 