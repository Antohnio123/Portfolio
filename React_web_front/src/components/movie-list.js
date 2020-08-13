import React from "react";
var FontAwesome = require('react-fontawesome');


function MovieList (props) {

    const movieClicked = movie => evt => {
        // функция, которая по евенту передаёт movie в другую функцию movieclicked,
        // ту, которая из App.js через props передана...
        props.movieClicked(movie)
    }
    const editClicked = movie => {
        props.editClicked(movie);
    }

    const removeMovie = movie => {
       //  Это такая же arrow-функция, но стрелка внизу, в самом ивенте.
        if (window.confirm("Are you sure, you want to DELETE this movie?")) {
            fetch(`${process.env.REACT_APP_API_URL}/api/movies/${movie.id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${this.props.token}` },
            })
                .then ( resp => props.movieDeleted(movie))
                .catch ( error => console.log(error))
        }
    };
    const newMovieCreate = () => {
        props.newMovie()
    };

    return (

        <div className="list"  >
            <FontAwesome name="plus" className="listed pushable" onClick={newMovieCreate}/>
            {/* ТУТ ОЧЕНЬ НУЖНО ДОБАВИТЬ ПОИСКОВУЮ СТРОКУ */}
            { props.movies.map( movie => {
                return (
                    <div key={movie.id} className="list-item">
                        <h3 className="listed pushable"  onClick={movieClicked(movie)}>
                            {/*по щелчку мыши мы передаём мувик в функцию movieClicked*/}
                            {movie.title}
                        </h3>
                        <div className="icons_block">
                            <FontAwesome name="edit" className="icons admin" onClick={() =>editClicked(movie)} />
                            <span>       </span>
                            {/* Другой способ записания arrow-функции (стрелка от ивента тут, а не в описании функции) */}
                            <FontAwesome name="trash" className="icons admin" onClick={() =>removeMovie(movie)}/>
                        </div>


                        {/*movie - объект, распаковываемый из json, поэтому ключом можно сделать id,*/}
                        {/*а выводить надо какое-то значение movie-объекта (словаря) по ключу*/}

                    </div>
                )})}
        </div>
    )
}

export default MovieList;