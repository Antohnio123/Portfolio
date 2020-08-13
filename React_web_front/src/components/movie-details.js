import React, { Component } from 'react';
// Другой способ импортировать библиотеку...
var FontAwesome = require('react-fontawesome');


class MovieDetails extends Component {
    state = {
        highlighted: -1,
    }

    highlightRate = high => evt => {
        this.setState({highlighted: high});
    }

    // Хорошо бы прописать логику для rateClicked, закрепляющую жёлтый или другой цвет звёздочек вплоть до той, на которую кликнули
    // А изначально должны подсвечиваться звёзды до уровня оценки текущего пользователя, подгружаемого из базы данных
    rateCLicked = stars => evt => {
        // Чтобы в строку запроса вставлять переменную, кавычки надо поставить те, что на тильде
        fetch(`${process.env.REACT_APP_API_URL}/api/movies/${this.props.movie.id}/rate_movie/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${this.props.token}` },
            // В отличие от учителя я прописал на сервере, что в рейтинге должен быть и текст комментария, так что его надо передать
            body: JSON.stringify({stars: stars+1, comment: ''})
        })
            // .then ( resp => resp.json())
            .then ( res => this.getDetails())
            .catch ( error => console.log(error))
    }

    getDetails = () => {
        // просто запускает родителя, а логика - там
        this.props.loadMovie(this.props.movie)
    }

    render () {
        const mov = this.props.movie;
        return (

                <div className="details">
                    { mov ?
                        <React.Fragment>
                            <h3>{mov.title}</h3>
                            {/*Тупой способ разместить 5 звёзд )))*/}
                            <FontAwesome name="star" className={mov.avg_rating > 0 ? 'orange' : ''}/>
                            <FontAwesome name="star" className={mov.avg_rating > 1 ? 'orange' : ''}/>
                            <FontAwesome name="star" className={mov.avg_rating > 2 ? 'orange' : ''}/>
                            <FontAwesome name="star" className={mov.avg_rating > 3 ? 'orange' : ''}/>
                            <FontAwesome name="star" className={mov.avg_rating > 4 ? 'orange' : ''}/>
                            - {mov.num_of_ratings} vote(s)
                            <p>{mov.description}</p>

                            <div className="rate-container">
                                <h2>Rate it!</h2>
                                {/*  Нормальный способ разместить звёзды - через цикл map по массиву из 5, где e - элемент, i - индекс   */}
                                {/* Подсвечиваем звёзды, индекс которых выше индекса this.state.highlighted */}
                                {/* передавая в state.highlighted индекс i, а подсвечивая все, что > i-1 */}
                                { [...Array(5)].map( (e,i) => {
                                    return <FontAwesome key={i} name="star" className={this.state.highlighted > i-1 ? 'yellow' : ''}
                                    onMouseEnter={ this.highlightRate(i) } onMouseLeave={ this.highlightRate(-1)} onClick={this.rateCLicked(i)}/>

                                })}
                            </div>
                        </React.Fragment>
                        : <React.Fragment>
                            <p>Choose the film from the list</p>
                        </React.Fragment>
                    }
                </div>

            )
}}

export default MovieDetails;