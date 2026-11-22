# ASimpleWYSIWYGEditor
A basic HTML/CSS WYSIWIG editor intended for making static web pages

## How to use it
The application is split in 5 sections:

(insert-image)

1. Toolbox
2. Live preview
3. Element and child element(s)
4. CSS properties
5. Element properties

-----------------------------------------------------------------

1. ### Adding a heading and a paragraph
    To add a heading, press the button labeled **Heading 1 (&lt;h1>)** in the *Text elements* section.
    
    To add a paragraph, press the button labeled **Paragraph (&lt;p>)** that is also in the *Text elements* section.

    To change the text of the heading or paragraph, click on one of them, click on the **Text element [1]** button that can be found in the section at the bottom of the application, and then change the value in the cell labeled **text** that can be found in the *Element properties* section. You should be able to see the change after clicking off the cell or after pressing **Enter**.
2. ### Adding an image
    To add an image, press on the button labeled **Image (&lt;img>)** in the *Media elements* section of the **Toolbox**.

    To set the source of the image, click on the **Add new...** button in the *Element properties* section. A new, blank property will be created. Set its name to *src* and its value to the URL of the image.

    You might want to adjust or remove the default height and width values of the image (also found in the *Element properties*). You can remove them by clicking on their name, pressing **Backspace** and then **Enter** (or click off).
3. ### Adding a content division (&lt;div>) and adding elements inside of it
    To add a content division, click on the button labeled **Content division (&lt;div>)**, under the *Page structure* section of the **Toolbox** (you are going to have to scroll down).

    To add elements inside of the content division, all you have to do is select it. New elements automatically get added inside of the last selected element.

    You might want to change or remove its height, width and/or border-style CSS properties. You can do that from the *CSS properties* section.
