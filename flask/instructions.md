## Current State
Right now, [app.py](./app.py) is the entry point for our flask app.
To start the app, run the following command from inside the `flask` directory:

```bash
flask --app app.py --debug run
```

The database that is in the folder right now, `./dbname.sqlite`, is a placeholder and should be deleted,
but it auto populates from the boilerplate for creating the SQLAlchemy session.

## Structure
The app hook into the `templates` directory and the `static` directory.
`static` holds CSS and Javascript files that will be statically served when the flask app is run.
`templates` holds HTML templates that will be populated with info and graphs from the database and our JS files.

As Leaflet and D3 require class hooks, pass the following div IDs into your functions:
- `map`
- `scatter`
- `radar`
- `slope`

## Passing Data Through
You will also need to access a JS object to get the data to manipulate.
I think Flask will pass all the data in as `query_results`.
Look in the [example JS file](./static/app.js) for an example of how the variable should be able to be accessed.

I'm working on something that would allow dynamic querying via routines.
That is what the second routine in  `app.py` is.
If you want a button other input to run another query (for example, getting a different dataset to refresh the maps),
I think we should be able to POST text,
parse it into python variables,
send that through SQLAlchemy,
and return new data to the `query_results` variable.
The downside looks like it would mean all tables would need to be refreshed.
The upside might be that we could click `back` to get to a previous visualization.
I don't know, still working this one out and will need to run some tests to see how it works.

## Design
I'm using [TailwindCSS](https://tailwindcss.com) for styling.
It uses utility classes, so you can style your elements however you want using it and they should all play nice with everyone else's.
I'm fine with switching back to [Bootstrap](https://getbootstrap.com) if anyone has an opinion one way or another.
I think Tailwind might be more modern (Bootstrap was originally created by Twitter and is now maintained by Github).
