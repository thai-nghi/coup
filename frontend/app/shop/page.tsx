"use client";

import Header from "@/components/header";
import { Carousel } from "antd";
import Image from 'next/image';
import registerImg from '@/assets/choi-co-up-12.jpg';
import ShopSection from "@/components/shop_section";

import "./index.scss"
import { useLocalStorageState, useRequest, useSessionStorageState } from "ahooks";
import { useState } from "react";
import { ShopSectionType } from "@/types";
import { buyItem, itemList } from "@/apis/shop";


const shopDataMock = [
    {
        name: "Chessboard",
        items: [
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            },
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            },
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            },
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            }
        ]
    },
    {
        name: "Chessback",
        items: [
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            },
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            },
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            },
            {
                id: 1,
                name: "Dragon Chessboard",
                description: "Chessboard used by emperors",
                price: 100,
                banner_pic: "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            }
        ]
    }
]


export default function Shop() {

    const [userData, setUserData] = useSessionStorageState("userData");
    const [authToken, setAuthToken] = useLocalStorageState("token");

    const [shopData, setShopData] = useState<ShopSectionType[]>();

    const { run: runBuyItem } = useRequest(buyItem, {
        manual: true,
        onSuccess: (result, params) => {
            console.log(result);
            userData.coins = result;
            setUserData(userData);

        },
    });

    useRequest(itemList, {
        onSuccess: (data, params) => {
            setShopData(data);
        },
        defaultParams: [authToken]
    })

    const clickByFunction = function(itemId: number){
        //runBuyItem(authToken, itemId);
        console.log("Buy item " + itemId);
    }

    return (
        <>
            <Header></Header>
            <div className="relative flex h-screen overflow-auto justify-center pb-16 pt-8 bg-primary-bg w-full">

                <div className="flex flex-col w-4/5 gap-5">

                    <Carousel className="overflow-hidden h-[300px]">
                        <Image src={registerImg} alt="" className="h-full" />
                        <Image src={registerImg} alt="" />
                    </Carousel>

                    <>
                        {shopDataMock.map((category) =>
                            <ShopSection name={category.name} items={category.items} clickBuyFn={clickByFunction} key={category.name}></ShopSection>
                        )}
                    </>


                </div>

            </div>
        </>
    )
}