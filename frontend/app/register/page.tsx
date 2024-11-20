"use client";

import type { FormProps } from 'antd';
import { Button, ConfigProvider, Form, Input, Select, Typography } from 'antd';
import Image from 'next/image';

import registerImg from '@/assets/choi-co-up-12.jpg';

export const validateMessages = {
    required: "${label} is required!",
    types: {
        email: "${label} is not a valid email!",
        number: "${label} is not a valid number!",
    },
    number: {
        range: "${label} must be between ${min} and ${max}",
    },
};

const { Title } = Typography;



type FieldType = {
    email?: string;
    display_name?: string;
    countr_id?: number;
    password: string;
    confirm_password: string;
};

const onFinish: FormProps<FieldType>['onFinish'] = (values) => {
    console.log("Submit", values);
}

export default function Register() {
    const [form] = Form.useForm();

    return (
        <>
            <section className="flex h-screen gap-4 p-8 bg-primary-bg">
                <ConfigProvider
                    theme={{
                        token: {
                            // Seed Token
                            colorPrimary: '#99B898',

                            // Alias Token
                            colorBgContainer: '#FF847C',

                            colorText: '#FFFFFF',
                            colorTextPlaceholder: '#FFFFFF'
                        },
                    }}
                >
                    <div className="mt-24 w-full p-16 lg:w-3/5">
                        {
                            <div>
                                <Title
                                    style={{
                                        margin: 0,
                                        marginBottom: 5,
                                        color: 'white'
                                    }}

                                >
                                    Welcome to Coup!
                                </Title>
                                <Title
                                    level={3}
                                    className="font-medium"
                                    style={{
                                        margin: 0,
                                        marginBottom: 20,
                                        color: 'white'
                                    }}
                                >
                                    Ready test your wit?
                                </Title>
                                <Form
                                    validateMessages={validateMessages}
                                    form={form}
                                    layout="vertical"
                                    onFinish={onFinish}
                                >
                                    <Form.Item
                                        required
                                        label="Email"
                                        rules={[
                                            {
                                                required: true,
                                                message: "Please input your Email!",
                                            },
                                        ]}
                                        name="email"
                                    >
                                        <Input type="email" placeholder="name@mail.com" />
                                    </Form.Item>
                                    <Form.Item
                                        required
                                        label="Display Name"
                                        rules={[
                                            {
                                                required: true,
                                                message: "Please select a display name",
                                            },
                                        ]}
                                        name="display_name"
                                    >
                                        <Input placeholder="MasterSlayerxXx" />
                                    </Form.Item>
                                    <Form.Item
                                        required
                                        label="Password"
                                        rules={[
                                            {
                                                required: true,
                                                message: "Please enter a password",
                                            },
                                        ]}
                                        name="password"
                                    >
                                        <Input type="password" />
                                    </Form.Item>
                                    <Form.Item
                                        required
                                        label="Password confirm"
                                        rules={[
                                            {
                                                required: true,
                                                message: "Please confirm your password",
                                            },
                                        ]}
                                        name="password_confirm"
                                    >
                                        <Input type="password" />
                                    </Form.Item>
                                    <div>
                                        <Form.Item
                                            label="Gender"
                                            required
                                            name="gender"
                                            rules={[
                                                {
                                                    required: true,
                                                },
                                            ]}
                                        >
                                            <Select
                                                allowClear
                                                placeholder="Please select"
                                            ></Select>
                                        </Form.Item>

                                    </div>
                                    <Form.Item>
                                        <Button
                                            color="primary"
                                            variant="solid"
                                            className="mt-5 w-full"
                                            type="primary"
                                            htmlType="submit"
                                        >
                                            Submit
                                        </Button>
                                    </Form.Item>
                                </Form>
                            </div>
                        }
                    </div>
                </ConfigProvider>
                <div className="fixed right-0 top-0 hidden h-screen w-2/5 text-center lg:block content-center p-6">
                    <Image src={registerImg} alt="">

                    </Image>

                </div>
            </section>

        </>
    )

}