"use client";

import { useLocalStorageState, useSessionStorageState } from "ahooks";
import Landing from "./landing";
import Link from "next/link";
import { Table } from "antd";
import Header from "./header";

import { faNetworkWired, faHandshake } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";


const matchColumns = [{
    title: 'Players',
    dataIndex: 'players',
    key: 'players',
},
{
    title: 'Elo',
    dataIndex: 'elo',
    key: 'elo',
}
];

const matches = [
    {
        players: "Li vs Chong",
        elo: 2400
    }
]

const rankingColumns = [
    {
        title: 'Rank',
        dataIndex: 'rank',
        key: 'rank',
    },
    {
        title: 'Player',
        dataIndex: 'player',
        key: 'player',
    },
    {
        title: 'Elo',
        dataIndex: 'elo',
        key: 'elo',
    }
]

const ranking = [
    {
        rank: 1,
        player: "Li",
        elo: 2550
    }
]

export default function HomePage() {

    const [userData, setUserData] = useSessionStorageState("userData");
    const [_, setUserToken] = useSessionStorageState("googleToken");
    const [authToken, setAuthToken] = useLocalStorageState("token");

    return (
        <>
            <Header></Header>
            <>
                {userData && (
                    <>
                        <div className="relative flex flex-col h-screen items-center gap-5 pb-16 pt-8 bg-primary-bg w-full">
                            <div className="container flex flex-col items-center justify-center h-2/5 gap-3 w-full">
                                <Link href="/login" className="flex self-center w-1/3">
                                    <div className="bg-primary-element rounded-md justify-center flex text-center p-3 px-12 w-full gap-5">
                                        <FontAwesomeIcon icon={faNetworkWired} size="2x" />
                                        <p className="bold text-3xl">Play Online</p>
                                    </div>
                                </Link>
                                <Link href="/login" className="flex self-center w-1/3">
                                    <div className="bg-primary-element rounded-md justify-center flex text-center p-3 px-12 w-full gap-5">
                                    <FontAwesomeIcon icon={faHandshake} size="2x" />
                                        <p className="bold text-3xl">Play With Friend</p>
                                        </div>
                                </Link>
                            </div>
                            <div className="container flex h-3/5 w-full px-16 justify-between">
                                <div className="conatiner h-full, w-1/3">
                                    <h1>Live Matches</h1>
                                    <Table dataSource={matches} columns={matchColumns} />
                                </div>
                                <div className="conatiner h-full, w-1/3">
                                    <h1>Leaderboard</h1>
                                    <Table dataSource={ranking} columns={rankingColumns} />
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </>

            {!userData && (
                <>
                    <div className="relative flex-col h-screen content-center justify-center pb-32 pt-8 bg-primary-bg">
                        <div className="container flex mx-auto bg-primary-element rounded-md h-full pb-32 pt-8 ">
                            <Landing></Landing>
                        </div>
                    </div>
                </>
            )}

        </>
    )
}