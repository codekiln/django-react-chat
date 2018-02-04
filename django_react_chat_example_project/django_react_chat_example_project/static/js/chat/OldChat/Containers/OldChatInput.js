import React from 'react'
// noinspection ES6UnusedImports
import faPaperPlane from '@fortawesome/fontawesome-free-solid/faPaperPlane'
import FontAwesomeIcon from '@fortawesome/react-fontawesome'


class OldChatInput extends React.PureComponent {

  constructor(props) {
    super(props)
    this.state = {
      textInput: ''
    }
    this.onTextChange = this.onTextChange.bind(this)
    this.onSubmit = this.onSubmit.bind(this)
  }

  onTextChange({target: {value: newText}}) {
    this.setState({textInput: newText})
  }

  onSubmit(event) {
    event.preventDefault()
    this.props.onSubmit(this.state.textInput)
    this.setState({'textInput': ''})
  }

  render() {

    return <form className="message-input" onSubmit={this.onSubmit}>
      <div className="wrap">
        <input type="text" placeholder="Write your message..." value={this.state.textInput}
               onChange={this.onTextChange}/>
        <button type="submit">
          <FontAwesomeIcon icon={faPaperPlane} />
        </button>
      </div>
    </form>
  }
}

export default OldChatInput
