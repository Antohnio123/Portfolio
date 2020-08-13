import React, { Component } from 'react';


class MovieForm extends Component {
    state = {
        editedMovie: this.props.movie,
        // перед тем, как мы изменили фильм, подгружается то, что он есть сейчас
        highlighted: -1,
        // savedMovie: this.props.movie,
    }
    cancelClicked = () => {
        // Просто запускает функцию родителя, переданную через props
        this.props.cancelForm()
    }
    inputChanged = event => {
        // На ходу при вводе данных передает инфу в локальный State
        // создаем локальную прееменную let movie
        let movie = this.state.editedMovie;
        movie[event.target.name] = event.target.value;
        // в локальной переменной movie выбирает ключ, равный имени элемента и даёт значение, равное value элемента
        // (а оно, видимо, само меняется от ивента onChange при вводе данных).
        this.setState({editedMovie: movie});
    }
    createClicked = () => {
        console.log(this.state.editedMovie);
        // Чтобы в строку запроса вставлять переменную, кавычки надо поставить те, что на тильде
        fetch(`${process.env.REACT_APP_API_URL}/api/movies/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${this.props.token}` },
            body: JSON.stringify(this.state.editedMovie)
        //    Передаём созданный editedMovie. ТУТ НУЖНО ВКЛЮЧИТЬ ПРОВЕРКУ ОТВЕТА!
            // ЕСЛИ BAD REQUEST, нужно сообщить, что не так и НЕ СОЗДАВАТЬ ЛОКАЛЬНО НОВУЮ СТРОЧКУ В list
        })
            .then ( resp => resp.json())
            .then ( res => this.props.addMovie(res))
            .catch ( error => console.log(error))
    }
    updateClicked = () => {
        fetch(`${process.env.REACT_APP_API_URL}/api/movies/${this.props.movie.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${this.props.token}` },
            body: JSON.stringify(this.state.editedMovie)
            //    Передаём созданный editedMovie
        })
            .then ( resp => resp.json())
            .then ( res => this.props.editedMovie(res))
            .catch ( error => console.log(error))
    }


    render () {
        const isDisabled = this.state.editedMovie.title.length === 0 ||
            this.state.editedMovie.description.length === 0;
        return (
            <div className="details">
                        <span>Title</span><br/>
                        <input type="text" name="title" value={this.props.movie.title}
                               onChange={this.inputChanged}/><br/>
                        <span>Description</span><br/>
                        <textarea  name="description" value={this.props.movie.description}
                                  onChange={this.inputChanged}/><br/>
                        { this.props.movie.id ?
                            <button disabled={isDisabled}  onClick={this.updateClicked}>Update</button>
                            : <button disabled={isDisabled} onClick={this.createClicked}>Create</button>}

                        <button onClick={this.cancelClicked}>Cancel</button>
                    </div>
        )
    }}

export default MovieForm;