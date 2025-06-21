import CMEditor from '@/components/cm-editor';


interface SolideContnetProps {
    profiles: string[];
    prompt?: string;
    model?: string;
    temperature?: number;
    other_conf?: any;
}

interface SolideContnet {

    isEdit: boolean;
    properties: SolideContnetProps;
    onChange: (properties: SolideContnetProps) => void;
    onBlur?: () => void;
    onEditChange?: (isEdit: boolean) => void;
}

export default function SolidContent(props: SolideContnet) {
    return (
        <CMEditor
            content={props.properties.prompt}
            profiles={props.properties.profiles}
            isEdit={props.isEdit}
            onBlur={props.onBlur}
            onChange={(value, isEdit) => {
                props.onChange({ ...props.properties, prompt: value })
                if (props.onEditChange) {
                    props.onEditChange(isEdit)
                }
            }}
        />

    )

}
