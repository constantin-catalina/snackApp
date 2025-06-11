import './CategoryList.css';

export function CategoryList(props){
    return (
        <div className="recipe-categories">
            {props.categories.map((cat, idx) => {
                return (
                    <div className="category-badge" 
                    style={{ backgroundColor: cat.color }}
                    key={`category-${idx}`}
                    >
                    {cat.name}
                    </div>
                );
            })}
        </div>
    );
}