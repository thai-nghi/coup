"use client";
import { useSessionStorageState, useRequest, useLocalStorageState } from "ahooks";
import { Avatar, ConfigProvider, Drawer } from "antd";
import Link from "next/link";
import { useEffect, useState } from "react";
import avatarImg from "@/assets/avatar.png"
import Image from 'next/image';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCrown, faCoins } from '@fortawesome/free-solid-svg-icons'

import { Typography } from 'antd';
import { UserData } from "@/types";
import { getUserInfo, matchHistorySummary } from "@/apis/user";

const { Title } = Typography;

export default function Header() {
    const [userData, setUserData] = useSessionStorageState<UserData>("userData", {listenStorageChange: true});
    const [historySummary, setHistorySummary] = useState();
    const [authToken, setAuthToken] = useLocalStorageState<string>("token");

    const [open, setOpen] = useState(false);

    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

    useRequest(matchHistorySummary, {
        onSuccess: (data, params) => {
            setHistorySummary(data);
        },
        defaultParams: [authToken!!]  ,
        ready: Boolean(authToken)
    })

    useEffect(() => {
        getUserInfo(authToken!!).then((res) => {
            setUserData(res);
        })
    }, [authToken])

    return (
        <>
            <div className="bg-fourth-element h-10 flex flex-row justify-between">
                <div className="w-24 h-full px-5 "><Link href="/" className="w-24 h-full flex"><p className="bold text-3xl text-third-element">Coup</p></Link></div>
                {!userData && (
                    <div className="w-24 h-full bg-third-element flex ">
                        <Link href="/login" className="w-24 h-full flex text-center justify-center"><p className="bold text-2xl">Login</p></Link>
                    </div>
                )}
                <>
                    {userData && (
                        <div className="w-1/8 h-full flex gap-5 justify-between">
                            <Link href="/shop" className="w-24 h-full flex text-center justify-center cursor-pointer bg-third-element"><p className="bold text-2xl">Shop</p></Link>
                            <div className="w-24 h-full flex text-center justify-center cursor-pointer bg-third-element" onClick={showDrawer}><p className="bold text-2xl">Profile</p></div>
                        </div>
                        
                    )}
                </>

                
            </div>
            <ConfigProvider
                theme={{
                    token: {
                        colorBgElevated: '#99B898',
                        colorText: '#FFFFFF'
                    },
                }}
            >
                <Drawer title="Profile" onClose={onClose} open={open}>
                    <div className="flex gap-1">
                        <div className="flex">
                            <Avatar size={128} src={<Image src={avatarImg} alt=""></Image>} />
                        </div>
                        <div className="flex flex-col">
                            <Title level={3} >{userData?.display_name}</Title>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faCrown} size="2x" /></div>
                                <p className="text-2xl">{userData?.elo}</p>
                            </div>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faCoins} size="2x" /></div>
                                <p className="text-2xl">{userData?.coins}</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-5 justify-center align-middle">
                        <p className="flex text-2xl">WINS: {historySummary?.win}</p>
                        <p className="flex text-2xl">LOSSES: {historySummary?.loss}</p>
                        {/* <Title className="flex" level={3} ></Title> 
                        <Title className="flex" level={3} >LOSSES: {historySummary?.loss}</Title> */}
                    </div>

                </Drawer>
            </ConfigProvider>
        </>
    )
}