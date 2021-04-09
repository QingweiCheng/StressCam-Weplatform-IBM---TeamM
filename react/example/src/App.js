import React, { Component } from 'react';
import './App.css';
import Todos from './components/Todos'

class App extends Component {
  state = {
    todos: [
      {
        id: 1,
        title: "milk",
        completed: false
      },
      {
        id: 2,
        title: "bread",
        completed: true
      },
      {
        id: 3,
        title: "eggs",
        completed: false
      },
    ]
  }
  render(){
    console.log(this.state.todos)
    return (
      <div>
        <Todos todos={this.state.todos} />
      </div>
    );
  }
}

export default App;
