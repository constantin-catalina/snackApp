import { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import { CategoryList } from '../components/CategoryList';
import './RecipePage.css';
import { DurationBadge } from '../components/DurationBadge';


export function RecipePage() {
  const { recipeId } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [servings, setServings] = useState(1);

  useEffect(() => {
    if (!recipeId) {
      return;
    }

    fetch(`${import.meta.env.VITE_API_URL}/recipes/${recipeId}`)  
      .then(async (res) => {
        const data = await res.json();

        if (!data.error) {
          setRecipe(data); 
        }
      })
      .catch((error) => console.error(error));
  }, [recipeId]);

  if (!recipe) {
    return (
      <div>
        Recipe not found
      </div>
    );
  }
  
  return (
    <>
      <h1>{recipe.name}</h1>
      <CategoryList categories={recipe.categories} />
      <DurationBadge duration={recipe.duration} />

      <h2>Ingredients</h2>
      <div>
        Servings:
        <input
          type="number"
          name="servings"
          value={servings}
          onChange={(event) => {
            const value = Number.parseInt(event.target.value, 10);
            setServings(value > 1 ? value : 1);
          }}
        />
      </div>
      <ul>
        {recipe.ingredients.map((ingredient) => {
          return (
            <li key={`recipe-${recipeId}-ingredient-${ingredient.id}`}>
              {ingredient.quantity * servings}{ingredient.unit} {ingredient.name}
            </li>
          );
        })}
      </ul>
      <div>
        <h2>Instructions</h2>
        <p>
          {recipe.instructions}
        </p>
      </div>
      <div className='gallery-section'>
        <h2>Pictures</h2>
        <div className="gallery">
          {recipe.pictures.map((pic, idx) => {
            return (
              <img src={pic} alt={recipe.name} key={`recipe-${recipeId}-image-${idx}`} />
            );
          })}
        </div>
      </div>
    </>
  );
}