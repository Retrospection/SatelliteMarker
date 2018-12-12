import React, { Component } from 'react';
import {
  Layout, Row, Col,
  Icon, Form, Button, Input,
  message
} from 'antd';
import styles from './App.module.css';

import { fetchImageById } from './api'; 

const {
  Header, Content,
} = Layout;
const FormItem = Form.Item;


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
    this.setState({
      imageUrl: "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2241666278,698607827&fm=26&gp=0.jpg"
    })
  }

  onLeftArrowClicked = () => {
    let newImageId = this.state.imageId - 1;
    if (newImageId < 0) {
      message.error("已经是第一张验证码了！")
      return;
    }
    getImageById('http://127.0.0.1:1260/captcha', this.imageId).then(json => {
      this.setState({
        imageUrl: json.data,
        imageId: newImageId
      })
    })
  }

  onRightArrowClicked = () => {
    let newImageId = this.state.imageId + 1;
    if (newImageId >= this.state.totalImages) {
      message.error("已经是最后一张验证码了！")
      return;
    } 
    getImageById('http://127.0.0.1:1260/captcha', 0).then(json => {
      this.setState({
        imageUrl: json.data,
        imageId: newImageId
      })
    })
  }


  onInputChange = (e) => {
    this.setState({
      inputValue: e.target.value
    })
  }

  onSubmitBtnClicked = (e) => {

  }

  onResetBtnClicked = (e) => {
    this.setState({
      inputValue: ""
    })
  }

  render() {
    return (
      <Layout>
        <Header className={styles.header}>新浪微博验证码标注工具</Header>
        <Content style={{backgroundColor: "white"}}>
          <Row type="flex" align="middle">
            <Col offset={9} span={1} style={{textAlign: "center"}}>
              <Icon className={styles.arrow} type="left" onClick={this.onLeftArrowClicked}/>
            </Col>
            <Col span={4}>
              <img alt="验证码图片" src={this.state.imageUrl} className={styles.captcha} />
            </Col>
            <Col span={1} style={{textAlign: "center"}}>
              <Icon className={styles.arrow} type="right" onClick={this.onRightArrowClicked}/>
            </Col>
          </Row>
          <div className={styles.form}>
            <div className={styles["form-items"]}>
              <Input value={this.state.inputValue} onChange={this.onInputChange} placeholder="请输入图片中的文字"/>
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
