import { useEffect, useState } from 'react';
import Select from 'react-select';

export function CategorySelect(props) {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/categories`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setOptions(data.map((el) => ({ label: el.name, value: el.id })));
      })
  }, []);

  return (
    <>
      <Select
        isMulti
        options={options}
        onChange={(newValues) => props.setCategories(newValues)}
      />
    </>
  )
}
