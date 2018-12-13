import React, { Component } from 'react';
import {
  Layout, Row, Col,
  Button, Input,
  message
} from 'antd';
import styles from './App.module.css';

import {
  fetchNextImage,
  fetchInitState,
  submitMark
} from './api';

const {
  Header, Content,
} = Layout;



class App extends Component {

  constructor (props) {
    super(props);
    this.state = {
      imageUrl: "",
      inputValue: "",
      imageId: 0,
      totalImages: 0
    };
  }

  componentDidMount() {
    fetchInitState('http://localhost:1260/init')
        .then(data => {
          const lastId = data.data.lastId;
          this.setState({
            imageId: lastId,
            totalImages: data.data.totalImages
          })
          return fetchNextImage('http://localhost:1260/captcha')
        })
        .then(data => {
          if (data.code === 0) {
            this.setState({
              imageUrl: data.data.imageUrl,
              imageId: data.data.imageId
            })
          }
        })
  }

  onInputChange = (e) => {
    this.setState({
      inputValue: e.target.value
    })
  }

  onSubmitBtnClicked = (e) => {
    submitMark('http://localhost:1260/mark', {
      imageId: this.state.imageId,
      markValue: this.state.inputValue
    }).then(data => {
      return fetchNextImage('http://localhost:1260/captcha')
    }).then(data => {
          if (data.code === 0) {
            this.setState({
              imageUrl: data.data.imageUrl,
              imageId: data.data.imageId,
              inputValue: "",
            })
          }
        })
  }

  onResetBtnClicked = (e) => {
    this.setState({
      inputValue: ""
    })
  }

  render() {
    return (
      <Layout>
        <Header className={styles.header}>新浪微博验证码标注工具 [ { this.state.imageId + 1 } / {this.state.totalImages} ]</Header>
        <Content style={{backgroundColor: "white"}}>
          <Row type="flex" align="middle">
            <Col offset={10} span={4}>
              <img alt="验证码图片" src={this.state.imageUrl} className={styles.captcha} />
            </Col>
          </Row>
          <div className={styles.form}>
            <div className={styles["form-items"]}>
              <Input value={this.state.inputValue} onChange={this.onInputChange} placeholder="请输入图片中的文字" onPressEnter={this.onSubmitBtnClicked}/>
            </div>
            <div className={styles["form-items"]}>
              <Button className={styles.btn} type="primary" onClick={this.onSubmitBtnClicked}>提交</Button>
              <Button className={styles.btn} onClick={this.onResetBtnClicked}>重置</Button>
            </div>
          </div>
        </Content>
      </Layout>
    );
  }
}

export default App;
