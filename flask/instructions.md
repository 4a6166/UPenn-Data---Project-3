## Current State
[app.py](./app.py) is the entry point for our flask app.
To start the app, run the following command from inside the `flask` directory:

```bash
flask --app app.py --debug run
```
The database is copied over from the SQLite folder.
It is the "production" database, and is where all the data will be pulled from and passed through to your HTML and JS files.

## Structure
The app hook into the `templates` directory and the `static` directory.

`static` holds CSS and Javascript files that will be statically served when the flask app is run.
It also holds images and icons or whatever static files you want severed.

`templates` holds HTML templates that will be populated with info and graphs from the database and our JS files.

## Passing Data Through
Every visual is using the same base HTML template, `vis.html`.
The Flask app uses a method called `render_template()` to pull the template and fill in placeholders.
The placeholders look like this: `{{ data | tojson }}`.
The first part of the placeholder is the variable that is being passed and the second is how it should be interpreted when being added to the HTML.

Below is an example of what full method call looks like:

```python
return render_template("vis.html", 
                       js=js_file,
                       css=css_file,
                       controls=controls,
                       data=data,
                       note=note,
                       attribution=attribution)
```

Here are how the variables are being used:

| HTML/JS Var | Python Var  | Use |
| ---         | ---         | --- |
| js          | js_file     | Passes the location of the JS file containing your visualization
| css         | css_file    | Passes the location of a CSS file you might need
| controls    | controls    | HTML for the any controls you need to manipulate your visualizations, such as dropdowns or radio buttons
| data        | data        | A variable passed to some JS in the HTML file, allows you to use the `data` var as if it was created by D3
| note        | note        | The notes, in HTML form, that you want shown on the right of the visualization
| attribution | attribution | The attribution or footnotes, in HTML, you want shown to the bottom right of the visualization


## Design
Use [TailwindCSS](https://tailwindcss.com) for styling.
It uses utility classes, so you can style your elements however you want using it and they should all play nice with everyone else's.
To add a style to your HTML, add a codes from Tailwind as classes in the raw HTML.

**Use Tailwind Classes before trying to use plain CSS files.**

This reduces some complexity, and the resulting compatibility issues, that occurs when populating the templates.
