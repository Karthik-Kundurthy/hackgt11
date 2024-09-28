import { FaArrowLeft } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

export default function ChatPage() {
  const messages: any = [
    {
      isUser: true,
      text: "Hi Harish!",
    },
    {
      isUser: false,
      text: "Hey whats up",
    },
  ];
  const inputValue = "";
  const handleInputChange = () => {};
  const handleSendMessage = () => {};
  const navigate = useNavigate();

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
          Harish
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

      <div className="flex items-center p-4 border-t w-full bg-secondary">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Type your message..."
          className="flex-1 p-2 rounded-lg border-none outline-none mr-3 text-md"
        />
        <button
          onClick={handleSendMessage}
          className="text-white font-bold py-2 px-4 rounded bg-primary hover:bg-primary-dark focus:outline-none focus:shadow-outline"
        >
          Send
        </button>
      </div>
    </div>
  );
}
