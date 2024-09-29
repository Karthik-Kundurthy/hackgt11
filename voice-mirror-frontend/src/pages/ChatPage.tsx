import { FaArrowLeft } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { ProfileContext } from "../contexts/ProfileContext";
import { Navigate } from "react-router-dom";
import { chat } from "../api/api";
import { useParams } from "react-router-dom";

export default function ChatPage() {
  const { name } = useParams();
  const { profile } = useContext(ProfileContext);
  const navigate = useNavigate();
  interface Message {
    isUser: boolean;
    text: string;
  }

  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const handleInputChange = (value: string) => {
    setInputValue(value);
  };
  const [isWaiting, setIsWaiting] = useState(false);
  const handleSendMessage = async (e: any) => {
    e.preventDefault();
    const newMessages = [
      ...messages,
      {
        isUser: true,
        text: inputValue,
      },
    ];
    setInputValue("");
    setMessages(newMessages);
    setIsWaiting(true);

    const response = await chat(inputValue);
    if (response.error) {
      alert(response.data);
    } else {
      console.log(response);
      newMessages.push({
        isUser: false,
        text: response.data.reply,
      });
      setMessages(newMessages);
      setIsWaiting(false);
    }
  };

  if (!profile) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex flex-1 flex-col bg-secondary w-full mx-auto rounded-lg overflow-hidden">
      <div className="flex justify-evenly border-b">
        <div className="flex-1 ml-3 flex items-center">
          <button
            className="bg-primaryButton text-primaryButtonText p-2 rounded-full"
            onClick={() => navigate("/")}
          >
            <FaArrowLeft />
          </button>
        </div>
        <div className="flex-1 p-4 bg-secondary text-center font-bold text-lg">
          {name}
        </div>
        <span className="flex-1"></span>
      </div>
      <div
        style={{
          flex: "1",
          overflowY: "auto",
          padding: "20px",
          background: "#ffffff",
        }}
      >
        {messages.map((message: any, index: any) => (
          <div
            key={index}
            className="mb-3"
            style={{
              textAlign: message.isUser ? "right" : "left",
            }}
          >
            <span
              className="inline-block p-3 rounded-lg mx-2 max-w-full break-words"
              style={{
                backgroundColor: message.isUser ? "#cee4fd" : "#e7f3ff",
                color: message.isUser ? "#0B5394" : "#333",
              }}
            >
              {message.text}
            </span>
          </div>
        ))}
      </div>

      <form className="flex items-center p-4 border-t w-full bg-secondary" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => handleInputChange(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-2 rounded-lg border-none outline-none mr-3 text-md"
        />
        <button
          type="submit"
          className="text-white font-bold py-2 px-4 rounded bg-primaryButton hover:bg-primary-dark focus:outline-none focus:shadow-outline"
          disabled={isWaiting}
        >
          Send
        </button>
      </form>
    </div>
  );
}
