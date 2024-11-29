export interface ShopItem {
    id: number;
    name: string;
    description: string;
    price: number;
    banner_pic: string;
}

export interface ShopSectionProps {
    name: string;
    items: ShopItem[];
    clickBuyFn: Function;
}
    
export interface ShopSectionType {
    name: string;
    items: ShopItem[];
}

export interface UserData {
    email: string;
    display_name: string;
    id: number;
    elo: number;
    coins: number;
}