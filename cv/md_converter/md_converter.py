import argparse
from pathlib import Path, PurePath
import markdown
import pdfkit
from pdfrw import PdfReader, PdfWriter, PdfName, PdfString


def change_extension(file_path, new_extension):
    return str(Path(file_path).with_suffix(new_extension))


DEF_MD = "CV.md"
DEF_OUT = "output"
DEF_CSS = "styles.css"
DEF_META = "metadata.txt"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("md_file", type=str, help="The name of the file to process")
    parser.add_argument(
        "--css", type=str, help="CSS style file to apply to output HTML"
    )
    parser.add_argument("--meta", type=str, help="Metadata file to apply to output PDF")
    parser.add_argument("--out-dir", type=str, help="Output path for all the artifacts")
    parser.add_argument("--out-name", type=str, help="Output pdf name")
    args = parser.parse_args()

    if not args.md_file:
        print("Input file is not provided, using default")
        args.md_file = DEF_MD
    if not args.out_dir:
        print("Output directory is not provided, using default")
        args.out_dir = DEF_OUT
    out_path = Path(args.out_dir)
    out_string = args.out_dir + "/"
    try:
        out_path.mkdir()
        print(f"Directory '{out_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{out_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{out_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    file_path = Path(args.md_file)
    if not file_path.exists() or not file_path.is_file():
        print("Input MD file does not exist")
        return
    print("Artifacts will be saved at " + str(Path(args.out_dir).absolute()))
    with open(args.md_file, "r") as i:
        print("Opening the input MD file " + args.md_file + "...")
        md_content = i.read()
    print("Adding header to HTML...")
    html_content = "<!DOCTYPE html>\n"
    html_content += "<html>\n"
    html_content += "<head>\n"
    html_content += '<meta charset="UTF-8"/>\n'
    if not args.css:
        print("CSS is not provided, using default")
        args.css = DEF_CSS
    file_path = Path(args.css)
    if file_path.exists() and file_path.is_file():
        with open(args.css, "r") as c:
            print("CSS file is " + args.css + " applying styles to HTML...")
            css_content = c.read()
            html_content += "<style>\n"
            html_content += css_content + "\n"
            html_content += "</style>\n"
    html_content += "</head>\n"
    html_content += "<body>\n"
    print("Converting MD buffer to HTML...")
    html_content += markdown.markdown(md_content)
    print("Adding footing to HTML...")
    html_content += "</body>\n"
    html_content += "</html>\n"
    html_file = change_extension(args.md_file, ".html")
    print("Saving HTML file...")
    with open(out_string + html_file, "w") as o:
        o.write(html_content)
    print("HTML file saved ")
    if not args.out_name:
        pdf_file = change_extension(args.md_file, ".pdf")
    else:
        pdf_file = args.out_name
    print("Converting HTML to PDF...")
    config = pdfkit.configuration(wkhtmltopdf=r"wkhtmltopdf.exe")
    pdf_path_string = out_string + pdf_file
    html_path_string = out_string + html_file
    pdfkit.from_file(
        html_path_string,
        pdf_path_string,
        configuration=config,
        options={"enable-local-file-access": "", "dpi": 600, "zoom": 1.1},
    )
    if not args.meta:
        print("Metadata file is not provided, using default")
        args.meta = DEF_META
    pdf_reader = PdfReader(pdf_path_string)
    file_path = Path(args.meta)
    if file_path.exists() and file_path.is_file():
        with open(file_path, "r") as m:
            print(
                "Metadata file is "
                + args.meta
                + " adding your awesome metadata to PDF..."
            )
            metadata = {}
            for line in m:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    metadata[PdfName(key.strip())] = PdfString(f"({value.strip()})")
            print("Adding our awesome metadata...")
            if metadata:
                pdf_reader.Info = metadata
            PdfWriter().write(pdf_path_string, pdf_reader)
    print("Finished!")
    print("Output HTML: " + str(Path(html_path_string).absolute()))
    print("Output PDF: " + str(Path(pdf_path_string).absolute()))


if __name__ == "__main__":
    main()
