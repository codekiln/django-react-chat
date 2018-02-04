import React, { Component } from 'react'
import { BatchHttpLink } from "apollo-link-batch-http"
import { InMemoryCache } from "apollo-cache-inmemory"
import { ApolloClient } from 'apollo-client'
import { ApolloProvider } from 'react-apollo'
import ChatGroupSelector from './Containers/ChatGroupSelector'
import ReactDOM from 'react-dom'


const apolloClient = new ApolloClient({
  link: new BatchHttpLink({ uri: 'http://localhost:8000/gql_batched' }),
  cache: new InMemoryCache(),
});


class ChatApp extends Component {
  render() {
    return (
      <ApolloProvider client={apolloClient}>
        <ChatGroupSelector/>
      </ApolloProvider>
    )
  }
}


const webpackBundleName = 'chat.chat_app'
const context = window.js_context[webpackBundleName]
const domNode = document.getElementById(webpackBundleName)

ReactDOM.render(
  <ChatApp {...context}/>
  , domNode)

export default ChatApp
