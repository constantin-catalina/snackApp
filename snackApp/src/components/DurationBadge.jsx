import './DurationBadge.css';
import hourglass from '../assets/hourglass.svg'

export function DurationBadge({ duration }) {
    return (
        <div className="recipe-duration">
            <img src={hourglass} alt="Cooking time" />
            {duration}
        </div>
    );
}