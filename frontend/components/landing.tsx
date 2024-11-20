"use client";
import { Button, Typography } from 'antd';

const { Title } = Typography;
export default function Landing() {
    return (
        <>
            <div className="container h-full w-full bg-amber-500 flex flex-col space-y-4 justify-center">
                <Title className="self-center">Chess, but with a gacha twist</Title>
                <div className="h-1/8 w-64 z-10 bg-green-300 rounded-md self-center content-center justify-center flex"><Title level={2}>Play Online</Title></div>
            </div >
        </>
    )
}