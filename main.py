from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.orm import sessionmaker, Session

# ---------------- DATABASE ----------------

engine = create_engine(
    "sqlite:///recipes.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[str] = mapped_column(String(50))
    ingredients: Mapped[str] = mapped_column(String(500))
    instructions: Mapped[str] = mapped_column(String(1000))


Base.metadata.create_all(bind=engine)

# ---------------- FASTAPI ----------------

app = FastAPI()

templates = Jinja2Templates(directory="frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- GET ----------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    recipes = db.scalars(select(Recipe)).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"recipes": recipes}
    )


# ---------------- CREATE ----------------

@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html"
    )


@app.post("/create")
def create_recipe(
        title: str = Form(...),
        category: str = Form(...),
        ingredients: str = Form(...),
        instructions: str = Form(...),
        db: Session = Depends(get_db)
):

    recipe = Recipe(
        title=title,
        category=category,
        ingredients=ingredients,
        instructions=instructions
    )

    db.add(recipe)
    db.commit()

    return RedirectResponse("/", status_code=303)


# ---------------- UPDATE ----------------

@app.get("/update/{recipe_id}", response_class=HTMLResponse)
def update_page(
        request: Request,
        recipe_id: int,
        db: Session = Depends(get_db)
):

    recipe = db.get(Recipe, recipe_id)

    return templates.TemplateResponse(
        request=request,
        name="update.html",
        context={"recipe": recipe}
    )


@app.put("/recipe/{recipe_id}")
def update_recipe_api(
        recipe_id: int,
        title: str,
        category: str,
        ingredients: str,
        instructions: str,
        db: Session = Depends(get_db)
):

    recipe = db.get(Recipe, recipe_id)

    if recipe:

        recipe.title = title
        recipe.category = category
        recipe.ingredients = ingredients
        recipe.instructions = instructions

        db.commit()

        return {"message": "Recipe Updated"}

    return {"message": "Recipe Not Found"}


@app.post("/update/{recipe_id}")
def update_recipe(
        recipe_id: int,
        title: str = Form(...),
        category: str = Form(...),
        ingredients: str = Form(...),
        instructions: str = Form(...),
        db: Session = Depends(get_db)
):

    recipe = db.get(Recipe, recipe_id)

    if recipe:
        recipe.title = title
        recipe.category = category
        recipe.ingredients = ingredients
        recipe.instructions = instructions

        db.commit()

    return RedirectResponse("/", status_code=303)


# ---------------- DELETE ----------------

@app.get("/delete/{recipe_id}", response_class=HTMLResponse)
def delete_page(
        request: Request,
        recipe_id: int,
        db: Session = Depends(get_db)
):

    recipe = db.get(Recipe, recipe_id)

    return templates.TemplateResponse(
        request=request,
        name="delete.html",
        context={"recipe": recipe}
    )


@app.delete("/recipe/{recipe_id}")
def delete_recipe_api(
        recipe_id: int,
        db: Session = Depends(get_db)
):

    recipe = db.get(Recipe, recipe_id)

    if recipe:
        db.delete(recipe)
        db.commit()
        return {"message": "Recipe Deleted"}

    return {"message": "Recipe Not Found"}

@app.post("/delete/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):

    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        return RedirectResponse("/", status_code=303)

    db.delete(recipe)
    db.commit()

    return RedirectResponse("/", status_code=303)