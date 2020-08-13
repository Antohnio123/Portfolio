import React, {Component} from 'react';
import './App.css';
import MovieList from "./components/movie-list";
import MovieDetails from "./components/movie-details";
import MovieForm from "./components/movie-edit-form";
import { withCookies } from "react-cookie";

var FontAwesome = require('react-fontawesome');



class App extends Component {
    state = {
        movies: [],
        // Оставим лист пустым, он будет наполняться с сервера Джанго через fetch data
        selectedMovie: null,
        // Как только одно из булевных значений перестает быть равно null, открывается описание фильма.
        editedMovie: null,
        savedMovie: null,
        // Token появляется тут после регистрации через login.js
        token: this.props.cookies.get('mr-token'),
    }

    componentDidMount() {
        if (this.state.token) {
            // fetch data /вставка данных по api из бэк-энда
            fetch(`${process.env.REACT_APP_API_URL}/api/movies/`, {
                method: 'GET',
                headers: {'Authorization': `Token ${this.state.token}` }
            }) // fetch is a promissed-based api, that means we can do "then"
                // .then ( resp => console.log(resp))
                .then ( resp => resp.json())
                // .then ( rest => console.log(rest))
                .then ( res => this.setState({movies: res}))
                .catch ( error => console.log(error))
        } else window.location.href="/";
    }

    loadMovie = movie => {
        // Перенес код подгрузки деталей из Муви-детаилс сюда
        fetch(`${process.env.REACT_APP_API_URL}/api/movies/${movie.id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token 719ba6c1082b4872ebebcb8c87bc9454e4b06fb2' },
        })
            .then ( resp => resp.json())
            .then ( res => this.setState({selectedMovie: res}))
            .catch ( error => console.log(error))
        // используется как для того чтобы показать данные по выбранному фильму, так и чтобы обновить их при отправке своего рейтинга или внесении изменений
        this.setState({editedMovie: null});
    }
    movieDeleted = selMovie => {
        // убирает УЖЕ удалённый с сервера мувик из списка
        const cleaned_movies = this.state.movies.filter( i_movie => i_movie.id !== selMovie.id );
        this.setState({movies: cleaned_movies, selectedMovie: null})
    }

    editClicked = editingMovie => {
        this.setState({editedMovie: editingMovie})
        // взять позицию editedMovie в листе movie, сохранить элемент этой позиции в savedMovie
        this.setState({SavedMovie: editingMovie})
        // this.setState({savedMovie: this.state.movies[this.state.posSavedMovie]})
    }
    newMovie = () => {
        this.setState({editedMovie: {title: 'New movie', description: ''}});
    }
    cancelForm = () => {
        // Вставить savedMovie на место в листе Movie, откуда он был взят.
        this.loadMovie(this.state.SavedMovie);
        //   ДОРАБОТАТЬ ДЛЯ ДОБАВЛЕНИЯ НОВОГО ФИЛЬМА!!!!   SAVED Movie получается undefined!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        // Ниже - строка кода учителя
        this.setState({editedMovie: null});
    }

    addMovie = addedMovie => {
        // добавляет только что созданный на сервере фильм в лист State.movie. Хорошо бы добавить уведомление alert или как там его...
        // И можно отфильтровать лист по дате публикации... если бы были фильтры.
        this.setState({movies: [...this.state.movies, addedMovie]});
    }


    render() {
        // в отличие от функции, класс должен рендерить элемент, а не просто возвращать. Мой хеадер сверху. ниже код учителя.
        return (
            <React.Fragment>
                <div className="App">
                    {/*<div className="header">*/}
                    {/*    <div className="header-left">*/}
                    {/*        <p className="pushable">Menu</p>*/}
                    {/*    /!*    ДОБАВИТЬ КНОПКИ МЕНЮ *!/*/}
                    {/*    </div>*/}
                    {/*    <div className="header-right">*/}
                    {/*        <p className="pushable" >{this.props.cookies.get('username')} </p>*/}
                    {/*        /!*    ДОБАВИТЬ переход в личный кабинет *!/*/}
                    {/*        <FontAwesome name="shopping-cart" className="pushable icons" />*/}
                    {/*    </div>*/}
                    {/*</div>*/}
                    <h1>
                        <FontAwesome name="film"/>
                        <span> Movie Rater</span>
                    </h1>
                    <div className="layout">
                        <MovieList movies={this.state.movies} movieClicked={this.loadMovie}
                        movieDeleted={this.movieDeleted} editClicked={this.editClicked}
                        newMovie={this.newMovie} token={this.state.token}/>
                        { this.state.editedMovie ?
                            <MovieForm movie={this.state.editedMovie} cancelForm={this.cancelForm} addMovie={this.addMovie}
                            editedMovie={this.loadMovie} token={this.state.token}/>
                            : <MovieDetails movie={this.state.selectedMovie} loadMovie={this.loadMovie} token={this.state.token}/>}
                    </div>
                </div>
            </React.Fragment>
        );
    }
}
export default withCookies(App);
