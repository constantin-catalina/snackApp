import { useState } from 'react';
import { Form, InputGroup, Modal } from 'react-bootstrap'
import { CategorySelect } from './CategorySelect';

export function AddRecipeModal(props) {
  const [name, setName] = useState('');
  const [duration, setDuration] = useState('')
  const [instructions, setInstructions] = useState('');
  const [ingredients, setIngredients] = useState([
    {
      unit: '',
      name: '',
      quantity: ''
    }
  ]);
  const [pictures, setPictures] = useState(['']);
  const [categories, setCategories] = useState([]);

  const handleIngredientsChange = (event, index) => {
    const { name, value } = event.target; // name matches the name prop on the input
    const newIngredients = [];

    for (let i = 0; i < ingredients.length; i++) {
      if (i !== index) {
        newIngredients.push(ingredients[i]);
      } else {
        const newItem = { ...ingredients[i] };
        if (name === 'quantity') {
          newItem.quantity = Number.parseFloat(value);
        } else {
          newItem[name] = value;
        }
        newIngredients.push(newItem);
      }
    }

    setIngredients(newIngredients);
  };

  const handlePicturesChange = (event, index) => {
    const { value: newPic } = event.target;
    const updatedPics = [...pictures];

    updatedPics[index] = newPic;
    setPictures(updatedPics);
  };

  const resetForm = () => {
    setName('');
    setDuration('')
    setInstructions('');
    setIngredients([
      {
        unit: '',
        name: '',
        quantity: ''
      }
    ]);
    setPictures(['']);
    setCategories([]);
    props.setShowAddModal(false);
  };

  const saveRecipe = async () => {
    const data = {
      name,
      duration,
      instructions,
      ingredients,
      pictures,
      categories: categories.map((c) => ({ name: c.label }))
    };

    try {
      await fetch(`${import.meta.env.VITE_API_URL}/recipes`, { 
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json'
        }
      });
    } catch (error) {
      console.log(error);
    } finally {
      resetForm();
    }

  };

  return (
    <Modal show={props.showAddModal} onHide={resetForm}>
        <Modal.Header closeButton>
          <Modal.Title>Add recipe</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form>
            <Form.Group className='mb-3'>
              <Form.Label>Title</Form.Label>
              <Form.Control type="text" placeholder="Title" value={name} onChange={(event) => setName(event.target.value)}/>
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>Duration</Form.Label>
              <Form.Control type="text" placeholder="Duration" value={duration} onChange={(event) => setDuration(event.target.value)} />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>
                Ingredients
              </Form.Label>
              {
                ingredients.map((ingredient, idx) => {
                  return (
                    <InputGroup key={`form-ingredient-${idx}`}>
                      <Form.Control name='quantity' placeholder='Quantity' value={ingredients[idx].quantity} onChange={(event) => { handleIngredientsChange(event, idx) }} />
                      <Form.Control name='unit' placeholder='Unit' value={ingredients[idx].unit} onChange={(event) => { handleIngredientsChange(event, idx) }} />
                      <Form.Control name='name' placeholder='Ingredient name' value={ingredients[idx].name} onChange={(event) => { handleIngredientsChange(event, idx) }} />
                      {ingredients.length > 1 && (
                        <button onClick={(event) => {
                          event.preventDefault();
                          const newIngredients = [];
                          
                          for (let i = 0; i < ingredients.length; i++) {
                            if (i !== idx) {
                              newIngredients.push(ingredients[i]);
                            }
                          }
                          setIngredients(newIngredients);
                        }}>
                          X
                        </button>
                      )}
                      <button onClick={(event) => {
                        event.preventDefault();
                        setIngredients([...ingredients, { unit: '', quantity: '', name: '' }])
                      }}>+</button>
                    </InputGroup>
                  )
                })
              }
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>Instructions</Form.Label>
              <Form.Control as="textarea" rows={3} value={instructions} onChange={(event) => setInstructions(event.target.value)} />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>
                Pictures
                <button
                  onClick={(event) => {
                    event.preventDefault();
                    setPictures([...pictures, '']);
                  }}
                  style={{ marginLeft: '16px' }}
                >
                  +
                </button>
              </Form.Label>
              {pictures.map((pic, idx) => {
                return (
                  <InputGroup>
                    <Form.Control
                      value={pic}
                      onChange={(event) => handlePicturesChange(event, idx)}
                      placeholder="Add a picture URL"
                    />
                    {pictures.length > 1 && (
                      <button onClick={(event) => {
                        event.preventDefault();
                        const updatedPics = [];

                        for (let i = 0; i < pictures.length; i++) {
                          if (i === idx) {
                            continue;
                          }
                          updatedPics.push(pictures[i]);
                        }
                        
                        setPictures(updatedPics);
                      }}>
                        X
                      </button>
                    )}
                  </InputGroup>
                );
              })}
            </Form.Group>
            <Form.Group>
              <Form.Label>Categories</Form.Label>
              <CategorySelect setCategories={setCategories} />
            </Form.Group>
          </Form>
        </Modal.Body>

        <Modal.Footer>
          <button className="secondary" onClick={() => resetForm()}>Cancel</button>
          <button onClick={saveRecipe}>Add</button>
        </Modal.Footer>
      </Modal>
  );
}