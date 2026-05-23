import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider, App as AntApp } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import App from './App'
import './styles/globals.css'

dayjs.locale('zh-cn')

const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    colorBgBase: '#ffffff',
  },
  components: {
    Menu: {
      darkItemBg: '#001529',
      darkItemColor: '#ffffff',
      darkItemSelectedBg: '#1890ff',
      darkItemSelectedColor: '#ffffff',
      darkBg: '#001529',
      darkSubMenuItemBg: '#000c17',
      darkItemHoverBg: '#1890ff20',
    },
    Layout: {
      siderBg: '#001529',
      headerBg: '#ffffff',
    },
  },
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider theme={theme} locale={zhCN}>
      <AntApp>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </AntApp>
    </ConfigProvider>
  </React.StrictMode>,
)
