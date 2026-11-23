# ASimpleWYSIWYGEditor
<img width="1570" height="835" src="https://github.com/user-attachments/assets/08af5e75-738b-474d-880c-e6a595000c65" />
A basic HTML/CSS WYSIWYG editor intended for making static web pages

## Download links
* ### Windows
    x86_64 binary --> [Download here](https://github.com/DevMa7e1/ASimpleWYSIWYGEditor/releases/download/v1.0.0/ASimpleWYSIWYGEditor-Windows.zip)

* ### Linux
    x86_64 binary --> [Download here](https://github.com/DevMa7e1/ASimpleWYSIWYGEditor/releases/download/v1.0.0/ASimpleWYSIWYGEditor-Linux.zip)

## How to use it
The application is split in 5 sections:
<img width="795" src="https://github.com/user-attachments/assets/d70a4339-27ee-44a0-ac9e-b50625d26db8" />

1. Toolbox
2. Live preview
3. Element and child element(s) sections
4. CSS properties
5. Element properties

These sections will be referred to by the names provided.

-----------------------------------------------------------------

1. ### Adding a heading and a paragraph
    To add a heading, press the button labeled **Heading 1 (&lt;h1>)** in the *Text elements* section of the Toolbox.
    
    To add a paragraph, press the button labeled **Paragraph (&lt;p>)** that is also in the *Text elements* section of the Toolbox.

    To change the text of the heading or paragraph, click on one of them, click on the **Text element [1]** button that can be found in the *child element(s) section* of the application, and then change the value in the cell labeled **text** that can be found in the *Element properties* section. You should be able to see the change after clicking off the cell or after pressing **Enter**.
2. ### Adding an image
    To add an image, press on the button labeled **Image (&lt;img>)** in the *Media elements* section of the Toolbox.

    To set the source of the image, click on the **Add new...** button in the *Element properties* section. A new, blank property will be created. Set its name to *src* and its value to the URL of the image.

    You might want to adjust or remove the default height and width values of the image (also found in the *Element properties*). You can remove them by clicking on their name, pressing **Backspace** and then **Enter** (or click off).
3. ### Adding a content division (&lt;div>) and adding elements inside of it
    To add a content division, click on the button labeled **Content division (&lt;div>)**, under the *Page structure* section of the Toolbox (you are going to have to scroll down).

    To add elements inside of the content division, all you have to do is select it. New elements automatically get added inside of the last selected element.

    You might want to change or remove its height, width and/or border-style CSS properties. You can do that from the *CSS properties* section.

> [!WARNING]
> When adding an element, always make sure that you are adding it to the correct parent. After selecting an element, you can go back to its parent by clicking on the **Go to parent** button.

## How to make the executables
### Linux
1. Install all necessary tools
    
    Debian and Debian-based distros:
    * `sudo apt install git python3-full`

    Arch Linux and Arch-based distros:
    * `sudo pacman -S git python`
2. `git clone https://github.com/DevMa7e1/ASimpleWYSIWYGEditor.git`
3. `cd ASimpleWYSIWYGEditor`
4. `python3 -m venv venv`
5. `source venv/bin/activate` (modify for your shell)
6. `pip install -r requirements.txt`
7. `pip install pyinstaller`
8. `python3 -m PyInstaller -F -n ASimpleWYSIWYGEditor main.py --add-data template.html:. --add-data translator.html:. --noconsole`

The resulting executable can be found in the **dist** folder.

## Windows
1. Install the latest version of Python
2. [Download the source code of ASimpleWYSIWYGEditor](https://github.com/DevMa7e1/ASimpleWYSIWYGEditor/archive/refs/heads/main.zip)
3. Unzip it and go into the created folder
4. Open a new CMD window
5. Copy the path of the previously opened folder and run the command `cd *your path here*`
6. Run the command `python -m venv venv`
7. Run the command `venv\Scripts\activate`
8. Run the command `pip install -r requirements.txt`
9. Run the command `pip install pyinstaller`
10. Run the command `python -m PyInstaller -F -n ASimpleWYSIWYGEditor --noconsole main.py --add-data template.html:. --add-data translator.html:.`

The resulting executable can be found in the **dist** folder.