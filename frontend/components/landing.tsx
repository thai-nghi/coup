"use client";
import { Typography } from 'antd';
import Link from 'next/link';

const { Title } = Typography;
export default function Landing() {
    return (
        <>
            <div className="container h-full w-full flex flex-col space-y-4 justify-center">
                <Title className="self-center">Chess, but with a gacha twist</Title>
                <Link href="/login" className="flex self-center">
                    <div className="bg-secondary-element rounded-md justify-center flex text-center p-3 px-12"><p className="bold text-3xl">Play Online</p></div>
                </Link>
                <div className="bg-secondary-element rounded-md self-center justify-center flex text-center p-3 px-6"><p className="bold text-xl">Play with a friend</p></div>
            </div >
        </>
    )
}