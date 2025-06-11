import {Modal, Form, FormGroup, FormControl} from 'react-bootstrap';
import {useState} from 'react';

export function AddCategoryForm(props){

    const [name, setName] = useState('');
    const [color, setColor] = useState('');

    const saveCategory = async () => {
        const data = {
            name: name,
            color: color
        }

        await fetch(`${import.meta.env.VITE_API_URL}/categories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        setName('');
        setColor('');
        props.handleClose();
    };

    return (
        <Modal show={props.show} onHide ={props.handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Add category</Modal.Title> 
            </Modal.Header>

            <Modal.Body>
                <Form>
                    <FormGroup>
                        <Form.Label>Category name</Form.Label>
                        <FormControl 
                        placeholder='Enter a category name' 
                        value={name} 
                        onChange = {(event) => {
                            setName(event.target.value);
                        }}
                        />
                    </FormGroup>
                    <FormGroup>
                        <Form.Label>Category color</Form.Label>
                        <FormControl 
                        type='color' 
                        value={color}
                        onChange={(event) => {
                            setColor(event.target.value);
                        }}
                        />
                    </FormGroup>
                </Form>

                <button onClick={saveCategory}>Add category</button>

            </Modal.Body>
        </Modal>
    );
}