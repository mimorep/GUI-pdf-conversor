import fitz
import os

from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import filedialog, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\\Proyectos\\GUI-pdf-conversor\\GUI\\build\\assets\\frame0")

###### Logic part ######

def save_pdf_pages (path, pageToPrint):
    
    folderName = "./convertedPDFs" 

    file = fitz.open(path)
    
    imageName = os.path.split(path)
    imageName = imageName[len(imageName) - 1]
    imageName = imageName.split('.')
    imageName = imageName[0]

    page = file.load_page(pageToPrint)
    pixel = page.get_pixmap()
    pageNumber = pageToPrint + 1

    # Check for the output folder
    if not os.path.exists(folderName):
        os.makedirs(folderName) 

    output = folderName + "/" + imageName + str(pageNumber) + ".png"
    
    pixel.save(output)
    file.close()

def get_pdf_pages (path):
    file = fitz.open(path)
    if file.is_pdf:
        pageCount = file.page_count
        file.close()
        return pageCount
    else:
        file.close()
        return 0
    
def parse_pdf (filepath):
    # Call the page counter
    pdf_pages = get_pdf_pages(filepath)

    try:
        count = 0
        
        while count < pdf_pages:
            # Now start parsing all the pdfs
            save_pdf_pages(filepath, count)
            count += 1

        os.system(f'start {os.path.realpath("./convertedPDFs")}')
        
    except:
        messagebox.showerror(title="Error", message="Error while parsing the pdfs files, please double check the format and the paths")

###### End Logic part ######


###### Buttons events ######

def folder_button_click ():
    # Get a folder picker and select the path
    folder_path = filedialog.askdirectory()

    # For each file with .pdf extension do the parsing event
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            # Check the file names
            filepath = subdir + os.sep + file

            if filepath.endswith(".pdf"):
                # Call the page counter
                pdf_pages = get_pdf_pages(filepath)

                parse_pdf(filepath=filepath)


def pdf_button_click ():
    file_paths = filedialog.askopenfilenames(
                        filetypes=[
                            ("PDF files", ".pdf")
                        ]
                    )

    for file_path in file_paths:
        # parse the pdf
        pdf_pages = get_pdf_pages(file_path)

        parse_pdf(file_path)
    
###### End Buttons events ######


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

ico = Image.open(relative_to_assets("AppIcon.png"))
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)
window.title("PDF2CSV")
window.geometry("300x400")
window.configure(bg = "#000000")

canvas = Canvas(
    window,
    bg = "#000000",
    height = 400,
    width = 300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=folder_button_click,
    relief="flat"
)
button_1.place(
    x=23.0,
    y=79.0,
    width=97.0,
    height=48.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=pdf_button_click,
    relief="flat"
)
button_2.place(
    x=169.0,
    y=79.0,
    width=97.0,
    height=48.0
)

canvas.create_rectangle(
    15.0,
    32.0,
    285.0,
    36.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    109.0,
    9.0,
    anchor="nw",
    text="PDF 2 PNG",
    fill="#FFFFFF",
    font=("RobotoRoman Medium", 14 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    150.0,
    274.0,
    image=image_image_1
)
window.resizable(False, False)
window.mainloop()
