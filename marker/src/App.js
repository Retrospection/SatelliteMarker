import React, { Component } from 'react';
import {
  Layout, Row, Col,
  Button, Input, message
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

const HOST = 'http://localhost:1260'

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
    fetchInitState(`${HOST}/init`)
        .then(data => {
          const lastId = data.data.lastId;
          this.setState({
            imageId: lastId,
            totalImages: data.data.totalImages
          })
          return fetchNextImage(`${HOST}/captcha`)
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

  onSubmitBtnClicked = () => {
    if (!/^[a-zA-Z0-9]{5}$/g.test(this.state.inputValue.length)) {
      message.error("请输入五个半角英文或数字字符！")
    }
    submitMark(`${HOST}/mark`, {
      imageId: this.state.imageId,
      markValue: this.state.inputValue
    }).then(data => {
      return fetchNextImage(`${HOST}/captcha`)
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
        <Header className={styles.header}>新浪微博验证码标注工具 [ 当前图片id: { this.state.imageId + 1 } / 总图片数：{this.state.totalImages} ]</Header>
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
