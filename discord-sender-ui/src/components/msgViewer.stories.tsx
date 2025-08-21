import type { Meta, StoryFn } from '@storybook/react';
import MsgViewer from './msgViewer';

export default {
    title: 'Components/MsgViewer',
    component: MsgViewer,
} as Meta<typeof MsgViewer>;

const Template: StoryFn<typeof MsgViewer> = (args) => <MsgViewer {...args} />;

export const Default = Template.bind({});
Default.args = {
    messages: [
        {
            time: '2025-08-21 10:00:00',
            content: 'Hello, this is a test message!',
            embedding: {
                link: 'https://example.com',
                image: 'https://pbs.twimg.com/media/GyqFdPGacAIB4mU.jpg:large',
                tags: ['example', 'test'],
                danbooru: 'https://danbooru.donmai.us',
            },
        },
        {
            time: '2025-08-21 11:00:00',
            content: 'Another message without embedding.',
        },
    ],
};