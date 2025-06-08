import React, {useEffect, useState} from 'react'

import {Card} from 'react-bootstrap';
import './HomePage.css'
import { CategoryList } from '../components/CategoryList';
import { DurationBadge } from '../components/DurationBadge';

export function HomePage() {

    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_API_URL}/recipes`)
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                setRecipes(data);
            })
    }, []);

    return (
        <>
            <h1>My recipes</h1>
            <div>
                Recipe count: {recipes.length}
            </div>
            <div className='recipes-container'>
                {
                    recipes.map((recipe) => {
                        return (
                            <Card key={`recipe-${recipe.id}`}>
                                <Card.Img src={recipe.pictures[0]} height={300}/>
                                <Card.Body>
                                    <Card.Title>
                                        {recipe.name}
                                    </Card.Title>
                                    <CategoryList categories={recipe.categories} />
                                    <DurationBadge duration={recipe.duration} />
                                </Card.Body>
                            </Card>
                        );
                    })
                }
            </div>
        </>
    );
}