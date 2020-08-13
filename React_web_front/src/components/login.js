import React, { Component } from 'react';
import{withCookies} from "react-cookie";


class Login extends Component {

    state = {
        credentials: {
            username: '',
            password: '',
            email: ''
        },
        serverAnswer: '',
        isLoginView: true,
        validate_password: '',
        justSigned: false,
    }

    inputChanged = event => {
       let user = this.state.credentials;
        user[event.target.name] = event.target.value;
        this.setState({credentials: user});
    }
    // По подобию сделал функцию ввода для repeat_password и email
    repeatPassword = event => {
        let repeat_password = this.state.validate_password;
        repeat_password = event.target.value;
        this.setState({validate_password: repeat_password});
    }
    inputEmail = event => {
        let user = this.state.credentials;
        user[event.target.name] = event.target.value;
        this.setState({credentials: user});
    }

    login = event => {
        // В зависимости от булевного значения isLoginView либо логинится, либо создаёт новый аккаунт
        if(this.state.isLoginView) {
            console.log(this.state.credentials);
            this.setState({justSigned: false});
            fetch(`${process.env.REACT_APP_API_URL}/auth/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify(this.state.credentials)
                //    Передаём credentials: логин и пароль
            })
                .then ( resp => resp.json())
                .then ( res => {
                    this.setState({serverAnswer: res});
                    console.log(res);
                    // ЕСЛИ ответ сервера содержит token, то переходим на главную.
                    // И записываем токен в куки.
                    if (res.token) {
                        window.location.href="/movies";
                        this.props.cookies.set('mr-token', res.token);
                        this.props.cookies.set('username', this.state.credentials.username);
                    }
                }).catch ( error => console.log(error))
        //  ЕСЛИ РЕГИСТРИРУЕМСЯ:
        }else {
            console.log(this.state.credentials);
            fetch(`${process.env.REACT_APP_API_URL}/api/users/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify(this.state.credentials)
                //    Передаём credentials: логин и пароль/ НАДО ДОБАВИТЬ ЕМЕЙЛ В BODY!
            })
                .then ( resp => resp.json())
                .then ( res => {
                    this.setState({serverAnswer: res});
                    this.setState({isLoginView: true});
                    this.setState({justSigned: true});
                }).catch ( error => console.log(error))
        }
    }

    toggleView = () => {
        this.setState({isLoginView: !this.state.isLoginView})
    }

    render() {
        return <div className="login-dark">
            <h1> {this.state.isLoginView ? 'Login' : 'Register' }</h1>
            <span className="app">Username</span><br/>
            <input type="login" name="username" value={this.state.credentials.username}
                   onChange={this.inputChanged}/><br/><br/>
            <p className="errorNote">{!this.state.justSigned ? this.state.serverAnswer.username: ''}</p>
            <span>Password</span><br/>
            <input type="password" name="password" value={this.state.credentials.password}
                   onChange={this.inputChanged}/><br/>
            <p className="errorNote">{!this.state.justSigned ? this.state.serverAnswer.password: ''}</p>
            {this.state.isLoginView ? <br/> :
                <div>
                    <span>Repeat password</span><br/>
                    <input type="password" name="repeat password" value={this.state.validate_password}
                       onChange={this.repeatPassword}/>
                    <br/>
                    <span>Email</span><br/>
                    <input type="text" name="email" value={this.state.credentials.email}
                           onChange={this.inputEmail}/>
                    <br/>
                </div>}


            <button onClick={this.login}>{this.state.isLoginView ? 'Login' : 'Register' }</button>
            <button onClick={this.toggleView}>{this.state.isLoginView ? 'Sign Up' : 'Allready have an account? Back to Login' }</button>
            <p className="errorNote">{this.state.serverAnswer.non_field_errors}</p>
        </div>
    }

}

export default withCookies(Login);


