import React, { useState } from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, useQuery, useMutation, gql } from '@apollo/client';

// Настройка Apollo Client для GitHub GraphQL API
const client = new ApolloClient({
  uri: 'https://api.github.com/graphql',
  cache: new InMemoryCache(),
  headers: {
    Authorization: `Bearer ${process.env.REACT_APP_GITHUB_TOKEN}`
  }
});

// GraphQL запросы
const GET_ISSUES = gql`
  query GetIssues($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      issues(first: 10, states: [OPEN]) {
        nodes {
          id
          title
          bodyText
          createdAt
          comments {
            totalCount
          }
          author {
            login
          }
        }
      }
    }
  }
`;

const ADD_COMMENT = gql`
  mutation AddComment($input: AddCommentInput!) {
    addComment(input: $input) {
      commentEdge {
        node {
          id
          body
          createdAt
        }
      }
    }
  }
`;

// Компонент для отображения списка issues
function IssuesList({ owner, name, onAddComment }) {
  const { loading, error, data } = useQuery(GET_ISSUES, {
    variables: { owner, name }
  });

  if (loading) return <div className="loading">Загрузка issues...</div>;
  if (error) return <div className="error">Ошибка: {error.message}</div>;

  const issues = data?.repository?.issues?.nodes || [];

  return (
    <div className="issues-list">
      <h2>Открытые issues в {owner}/{name}</h2>
      {issues.length === 0 ? (
        <p>Нет открытых issues</p>
      ) : (
        issues.map(issue => (
          <IssueItem key={issue.id} issue={issue} onAddComment={onAddComment} />
        ))
      )}
    </div>
  );
}

// Компонент для отдельного issue
function IssueItem({ issue, onAddComment }) {
  const [showCommentForm, setShowCommentForm] = useState(false);
  const [comment, setComment] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddComment(issue.id, comment);
    setComment('');
    setShowCommentForm(false);
  };

  return (
    <div className="issue-card">
      <h3>{issue.title}</h3>
      <p className="issue-meta">
        Автор: {issue.author?.login} | 
        Создано: {new Date(issue.createdAt).toLocaleDateString()} |
        Комментариев: {issue.comments.totalCount}
      </p>
      <p className="issue-body">{issue.bodyText.substring(0, 200)}...</p>
      
      <button onClick={() => setShowCommentForm(!showCommentForm)}>
        {showCommentForm ? 'Отмена' : 'Добавить комментарий'}
      </button>

      {showCommentForm && (
        <form onSubmit={handleSubmit} className="comment-form">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Введите комментарий..."
            rows="3"
            required
          />
          <button type="submit">Отправить</button>
        </form>
      )}
    </div>
  );
}

// Главный компонент приложения
function AppContent() {
  const [repo, setRepo] = useState('');
  const [searchParams, setSearchParams] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!repo.match(/^.+\/.+$/)) {
      setError('Пожалуйста, введите репозиторий в формате "owner/repo"');
      return;
    }
    setError('');
    const [owner, name] = repo.split('/');
    setSearchParams({ owner, name });
  };

  const handleAddComment = (issueId, body) => {
    console.log('Добавление комментария:', { issueId, body });
    // Здесь будет мутация для добавления комментария
    alert('Функция добавления комментария будет реализована позже');
  };

  return (
    <div className="app">
      <h1>GitHub Issues Manager</h1>
      
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={repo}
          onChange={(e) => setRepo(e.target.value)}
          placeholder="facebook/react"
          className="repo-input"
        />
        <button type="submit" className="search-button">
          Найти issues
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {searchParams && (
        <IssuesList 
          owner={searchParams.owner} 
          name={searchParams.name}
          onAddComment={handleAddComment}
        />
      )}
    </div>
  );
}

// Оборачиваем в ApolloProvider
function App() {
  return (
    <ApolloProvider client={client}>
      <AppContent />
    </ApolloProvider>
  );
}

export default App;