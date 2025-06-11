import './Navbar.css';

function Navbar(props) {
    return (
        <nav>
            <div className="logo">
                <a href="/">FullSnack</a>
            </div>
            <div className="buttons">
              <button onClick={props.onAddCategory}>
                + Add category
              </button>
              <button onClick={props.onAddRecipe}>
                  + Add recipe
              </button>
            </div>
        </nav>
    );
}

export { Navbar };