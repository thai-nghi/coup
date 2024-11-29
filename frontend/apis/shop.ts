import { send_request } from "./util";

export async function itemList(token: string) {
    const data = await send_request({
        method: "GET",
        url: `/shop`,
        token
    });

    return data?.data;
}

export async function buyItem(token: string, itemId: number) {
    const data = await send_request({
        method: "POST",
        url: `/shop/${itemId}`,
        token
    });

    return data?.data;
}

