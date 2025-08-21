import { Collapse } from 'antd';

const { Panel } = Collapse;

type Message = {
    time: string;
    content: string;
    embedding?: {
        link: string;
        image: string;
        tags?: string[];
        danbooru?: string;
    };
};

const MsgViewer = (messages: Message[]) => {
    return (
        <Collapse>
            {messages.map((message, index) => (
                <Panel header={`Message at ${message.time}`} key={index}>
                    <div>
                        <p>{message.content}</p>
                        {message.embedding && (
                            <div>
                                <p>Link: <a href={message.embedding.link} target="_blank" rel="noopener noreferrer">{message.embedding.link}</a></p>
                                <img src={message.embedding.image} alt="Embedded content" style={{ maxWidth: '100%' }} />
                                {message.embedding.tags && (
                                    <p>Tags: {message.embedding.tags.join(', ')}</p>
                                )}
                                {message.embedding.danbooru && (
                                    <p>Danbooru: {message.embedding.danbooru}</p>
                                )}
                            </div>
                        )}
                    </div>
                </Panel>
            ))}
        </Collapse>
    );
};

export default MsgViewer;