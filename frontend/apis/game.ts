import { send_request } from "./util";

export async function liveMatches(token: string, current: number = 1, pageSize: number = 10){
    return await send_request({
        method: "GET",
        url: '/game/lobby',
        token,
        params: {page: current, page_size: pageSize}
    })
}