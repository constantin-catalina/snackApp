import { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import './RecipePage.css';

export function RecipePage() {
  const { recipeId } = useParams();
  const [recipe, setRecipe] = useState(null); // use this state to display recipe info
  const [servings, setServings] = useState(1); // use this state to multiply ingredient quantities

  useEffect(() => {
    // send a GET request to the get recipe by id endpoint
    // and use the response to update the recipe state
  }, [recipeId]);

  if (!recipe) {
    // Show a message on the page that the recipe wasn't found
  }
  
  return (<></>);
}
