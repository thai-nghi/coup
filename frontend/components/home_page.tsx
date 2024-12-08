"use client";

import { useLocalStorageState, useSessionStorageState } from "ahooks";
import Landing from "./landing";
import Link from "next/link";
import { GetProp, Table, TableProps } from "antd";
import Header from "./header";

import { faNetworkWired, faHandshake } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useState } from "react";
import { liveMatches } from "@/apis/game";
import Image from 'next/image'


type ColumnsType<T extends object = object> = TableProps<T>['columns'];
type TablePaginationConfig = Exclude<GetProp<TableProps, 'pagination'>, boolean>;

interface TableParams {
    pagination?: TablePaginationConfig;
}

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
    },
    {
        rank: 2,
        player: "Matti",
        elo: 2500
    },
    {
        rank: 3,
        player: "Elina",
        elo: 2450
    },
    {
        rank: 4,
        player: "Arto",
        elo: 2425
    },
    {
        rank: 5,
        player: "Kaisa",
        elo: 2400
    },
    {
        rank: 6,
        player: "Ville",
        elo: 2375
    },
    {
        rank: 7,
        player: "Juha",
        elo: 2350
    },
    {
        rank: 8,
        player: "Noora",
        elo: 2325
    },
    {
        rank: 9,
        player: "Tuomas",
        elo: 2300
    },
    {
        rank: 10,
        player: "Sanna",
        elo: 2250
    },
    {
        rank: 11,
        player: "Eero",
        elo: 2200
    }
];

export default function HomePage() {

    const [userData, setUserData] = useSessionStorageState("userData", {listenStorageChange: true});
    const [_, setUserToken] = useSessionStorageState("googleToken");
    const [authToken, setAuthToken] = useLocalStorageState<string>("token");
    const [liveMatchData, setLiveMatchData] = useState();
    const [matchesLoading, setMatchLoading] = useState<boolean>(false);


    const [matchTableParam, setMatchTableParams] = useState<TableParams>({
        pagination: {
            current: 1,
            pageSize: 10,
        },
    });

    const fetchLiveMatches = () => {
        setMatchLoading(true);
        liveMatches(authToken!!, matchTableParam.pagination?.current, matchTableParam.pagination?.pageSize,).then((res) => {
            console.log(res);
            setMatchLoading(false);
            setLiveMatchData(res.map((entry) => {
                return {
                    players: `${entry.player_data[0].display_name} vs ${entry.player_data[1].display_name}`,
                    elo: Math.floor((entry.player_data[0].elo + entry.player_data[1].elo) / 2)
                }
            }))
        })
    }


    useEffect(fetchLiveMatches, [
        matchTableParam.pagination?.current,
        matchTableParam.pagination?.pageSize,
    ])

    const handleMatchTableChange = (pagination) => {
        setMatchTableParams({
            pagination,
        });

        // `dataSource` is useless since `pageSize` changed
        if (pagination.pageSize !== matchTableParam.pagination?.pageSize) {
            setLiveMatchData([]);
        }
    };

    return (
        <>
            <Header></Header>
            <>
                {userData && (
                    <>
                        <div className="relative flex flex-col h-screen items-center gap-5 pb-16 pt-8 bg-primary-bg w-full">
                            <div className="container flex h-2/5 w-full gap-5">
                                <div className="flex w-1/2 justify-end">
                                    <img src="https://greenify.host/storage/temporary/ss1.png" alt="Picture of chessboard"></img>
                                </div>
                                <div className="flex flex-col items-center justify-center h-full gap-3 w-1/2">
                                    <Link href="/game" className="flex self-center w-4/5">
                                        <div className="bg-primary-element rounded-md justify-center flex text-center p-3 px-12 w-full gap-5">
                                            <FontAwesomeIcon icon={faNetworkWired} size="2x" />
                                            <p className="bold text-3xl">Play Online</p>
                                        </div>
                                    </Link>
                                    <Link href="/game" className="flex self-center w-4/5">
                                        <div className="bg-primary-element rounded-md justify-center flex text-center p-3 px-12 w-full gap-5">
                                            <FontAwesomeIcon icon={faHandshake} size="2x" />
                                            <p className="bold text-3xl">Play With Friend</p>
                                        </div>
                                    </Link>
                                </div>
                            </div>
                            
                            <div className="container flex h-3/5 w-full px-16 justify-between">
                                <div className="conatiner h-full, w-1/3">
                                    <h1>Live Matches</h1>
                                    <Table dataSource={liveMatchData} columns={matchColumns} loading={matchesLoading} onChange={handleMatchTableChange} pagination={{defaultPageSize: 6}}/>
                                </div>
                                <div className="conatiner h-full, w-1/3">
                                    <h1>Leaderboard</h1>
                                    <Table dataSource={ranking} columns={rankingColumns} pagination={{defaultPageSize: 6}}/>
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