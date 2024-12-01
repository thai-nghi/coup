"use client";

import { Avatar, ConfigProvider } from "antd";
import avatarImg from "@/assets/avatar.png"
import Image from 'next/image';
import { Typography } from 'antd';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCrown, faClock, faBriefcaseClock } from '@fortawesome/free-solid-svg-icons'
import { useState } from "react";
import { useInterval } from "ahooks";

const { Title } = Typography;


interface MatchPlayerData {
    displayName: string;
    avatar: string;
    elo: number;
}

function secondsTo2DigitTime(seconds: number) {
    const min = Math.floor(seconds / 60);
    const sec = seconds - (min * 60);

    return `${min < 10 ? '0' + min : min}:${sec < 10 ? '0' + sec : sec}`
}

export default function MatchProfile({ displayName, avatar, elo }: MatchPlayerData) {
    
    const [roundTime, setRoundTime] = useState<number>(60);

    useInterval(() => {
        if (roundTime >= 0) {
            setRoundTime(roundTime - 1);
        }
    }, 1000);
    
    return (
        <>
            <ConfigProvider
                theme={{
                    token: {
                        colorBgElevated: '#99B898',
                        colorText: '#FFFFFF'
                    },
                }}
            >
                <div className="flex flex-row h-full w-fll pt-5 min-w-fit">
                    <div className="flex gap-2">
                        <div className="flex">
                            <Avatar size={128} src={<Image src={avatarImg} alt=""></Image>} />
                        </div>
                        <div className="flex flex-col">
                            <Title level={3} >{displayName}</Title>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faCrown} size="2x" /></div>
                                <p className="text-2xl">{elo}</p>
                            </div>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faClock} size="2x" /></div>
                                <p className="text-2xl">{secondsTo2DigitTime(roundTime)}</p>
                            </div>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faBriefcaseClock} size="2x" /></div>
                                <p className="text-2xl">{secondsTo2DigitTime(60*12)}</p>
                            </div>
                        </div>
                    </div>
                </div>

            </ConfigProvider>

        </>
    )
}