import './NavBar.css'

export function NavBar (props) {
    return (
        <nav>
            <div>
                FullSnack
            </div>
            <div>
                <button onClick={() => props.handleOpenCategoryModal()}>+ Add category</button>
                <button>+ Add recipe</button>
            </div>
        </nav>
    )
}