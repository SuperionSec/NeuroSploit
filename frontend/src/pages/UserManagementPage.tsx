import { useState, useEffect } from 'react'
import { message, Modal } from 'antd'
import {
  ProTable,
  ProColumns,
  ActionType,
  ModalForm,
  ProFormText,
  ProFormSelect,
  ProFormSwitch,
} from '@ant-design/pro-components'
import { PlusOutlined, UserOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons'
import { authApi, User, UserCreate, UserUpdate } from '../services/api'

export default function UserManagementPage() {
  const [loading, setLoading] = useState(false)
  const [actionRef, setActionRef] = useState<ActionType>()

  const columns: ProColumns<User>[] = [
    {
      title: '用户名',
      dataIndex: 'username',
      render: (text, record) => (
        <div className="flex items-center gap-2">
          <UserOutlined />
          <span>{text}</span>
        </div>
      ),
    },
    {
      title: '邮箱',
      dataIndex: 'email',
    },
    {
      title: '角色',
      dataIndex: 'role',
      valueEnum: {
        admin: { text: '管理员', status: 'Success' },
        user: { text: '用户', status: 'Default' },
      },
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      valueEnum: {
        true: { text: '启用', status: 'Success' },
        false: { text: '禁用', status: 'Error' },
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      valueType: 'dateTime',
    },
    {
      title: '操作',
      valueType: 'option',
      key: 'option',
      render: (_, record, __, action) => [
        <a
          key="edit"
          onClick={() => {
            setEditingUser(record)
            setEditModalVisible(true)
          }}
        >
          <EditOutlined /> 编辑
        </a>,
        <a
          key="delete"
          onClick={async () => {
            Modal.confirm({
              title: '确认删除',
              content: `确定要删除用户 "${record.username}" 吗？`,
              onOk: async () => {
                try {
                  setLoading(true)
                  await authApi.deleteUser(record.id)
                  message.success('删除成功')
                  action?.reload()
                } catch (err) {
                  console.error('Error deleting user:', err)
                  message.error('删除失败')
                } finally {
                  setLoading(false)
                }
              },
            })
          }}
        >
          <DeleteOutlined /> 删除
        </a>,
      ],
    },
  ]

  const [createModalVisible, setCreateModalVisible] = useState(false)
  const [editModalVisible, setEditModalVisible] = useState(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)

  const handleCreate = async (values: UserCreate) => {
    try {
      setLoading(true)
      await authApi.createUser(values)
      message.success('创建成功')
      actionRef?.reload()
      setCreateModalVisible(false)
    } catch (err) {
      console.error('Error creating user:', err)
      message.error('创建失败')
      return false
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = async (values: UserUpdate) => {
    if (!editingUser) return

    try {
      setLoading(true)
      await authApi.updateUser(editingUser.id, values)
      message.success('更新成功')
      actionRef?.reload()
      setEditModalVisible(false)
    } catch (err) {
      console.error('Error updating user:', err)
      message.error('更新失败')
      return false
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <ProTable<User>
        headerTitle="用户管理"
        actionRef={setActionRef}
        columns={columns}
        rowKey="id"
        pagination={{ pageSize: 10 }}
        request={async () => {
          const data = await authApi.listUsers()
          return { data, success: true }
        }}
        toolBarRender={() => [
          <button
            type="button"
            key="button"
            className="ant-btn ant-btn-primary"
            onClick={() => setCreateModalVisible(true)}
          >
            <PlusOutlined /> 新建用户
          </button>,
        ]}
      />

      <ModalForm
        title="新建用户"
        open={createModalVisible}
        onOpenChange={setCreateModalVisible}
        onFinish={handleCreate}
        submitter={{ searchConfig: { submitText: '创建' } }}
      >
        <ProFormText
          name="username"
          label="用户名"
          placeholder="请输入用户名"
          rules={[{ required: true, message: '请输入用户名' }]}
        />
        <ProFormText
          name="email"
          label="邮箱"
          placeholder="请输入邮箱"
          rules={[
            { required: true, message: '请输入邮箱' },
            { type: 'email', message: '请输入有效的邮箱' },
          ]}
        />
        <ProFormText.Password
          name="password"
          label="密码"
          placeholder="请输入密码"
          rules={[{ required: true, message: '请输入密码' }]}
        />
      </ModalForm>

      {editingUser && (
        <ModalForm
          title="编辑用户"
          open={editModalVisible}
          onOpenChange={setEditModalVisible}
          initialValues={editingUser}
          onFinish={handleEdit}
          submitter={{ searchConfig: { submitText: '更新' } }}
        >
          <ProFormText
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          />
          <ProFormText
            name="email"
            label="邮箱"
            placeholder="请输入邮箱"
            rules={[
              { required: true, message: '请输入邮箱' },
              { type: 'email', message: '请输入有效的邮箱' },
            ]}
          />
          <ProFormText.Password
            name="password"
            label="新密码（留空不修改）"
            placeholder="请输入新密码"
          />
          <ProFormSelect
            name="role"
            label="角色"
            options={[
              { value: 'admin', label: '管理员' },
              { value: 'user', label: '用户' },
            ]}
            placeholder="请选择角色"
          />
          <ProFormSwitch
            name="is_active"
            label="启用状态"
          />
        </ModalForm>
      )}
    </div>
  )
}
