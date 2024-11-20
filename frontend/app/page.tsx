import Landing from "@/components/landing";
import { List, ListItem, Card, Progress } from "@/components/mt-wrapper/mt-wrapper";
import { Button, Typography } from 'antd';

const { Title } = Typography;

export default function Home() {
  return (
    <>
      <div className="bg-white h-10 flex flex-row justify-between">
        <div className="w-24 h-full bg-amber-500">Home</div>
        <div className="w-24 h-full bg-amber-500">Login</div>
      </div>
      <div className="relative flex h-screen content-center items-center justify-center pb-32 pt-8">
        <div className="container flex mx-auto bg-white rounded-md h-full pb-32 pt-8 ">
          <Landing></Landing>
        </div>
      </div>
    </>
  );
}
