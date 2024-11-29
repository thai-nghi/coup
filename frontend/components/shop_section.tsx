"use client";

import {Button, Card, ConfigProvider, List, Typography } from "antd";
import { faCoins } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ShopSectionProps } from "@/types";

const { Title } = Typography;



export default function ShopSection({ name, items, clickBuyFn }: ShopSectionProps) {

    return (
        <>
            <ConfigProvider
                theme={{
                    token: {
                        colorPrimary: '#FF847C',
                        colorBgContainer: '#99B898',
                        colorText: '#FFFFFF'
                    },
                }}
            >
                <div className="flex flex-col w-full">
                    <Title level={1}>{name}</Title>

                    <div className="flex flex-row gap-5 pt-5">
                        <List
                            grid={{ gutter: 16, column: 3 }}
                            dataSource={items}
                            rowKey={(item) => item.id}
                            renderItem={(item) => (
                                <List.Item>
                                    <Card
                                    style={{ width: 300, minWidth: 300 }}
                                    cover={
                                        <img
                                            alt="example"
                                            src={item.banner_pic}
                                        />
                                    }
                                    actions={[
                                        <Button type="primary" onClick={() => clickBuyFn(item.id)}><FontAwesomeIcon icon={faCoins} size="2x" />{item.price}</Button>
                                    ]}
                                >
                                    <Title level={3}>{item.name}</Title>
                                    <h2>{item.description}</h2>

                                </Card>
                                </List.Item>
                            )}
                        />
                    </div>
                </div>
            </ConfigProvider>


        </>
    )
}