import React from 'react';
import { oneOf, bool, number, string, func } from 'prop-types';
import { Controlled as ReactCodeMirror } from 'react-codemirror2';
import styled from 'styled-components';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/yaml/yaml';
import 'codemirror/mode/jinja2/jinja2';
import 'codemirror/lib/codemirror.css';

const LINE_HEIGHT = 24;
const PADDING = 12;

const CodeMirror = styled(ReactCodeMirror)`
  && {
    height: initial;
    padding: 0;
  }

  & > .CodeMirror {
    height: ${props => props.rows * LINE_HEIGHT + PADDING}px;
    font-family: var(--pf-global--FontFamily--monospace);
  }

  ${props =>
    props.hasErrors &&
    `
    && {
      --pf-c-form-control--PaddingRight: var(--pf-c-form-control--invalid--PaddingRight);
      --pf-c-form-control--BorderBottomColor: var(--pf-c-form-control--invalid--BorderBottomColor);
      padding-right: 24px;
      padding-bottom: var(--pf-c-form-control--invalid--PaddingBottom);
      background: var(--pf-c-form-control--invalid--Background);
      border-bottom-width: var(--pf-c-form-control--invalid--BorderBottomWidth);
    }`}

  ${props =>
    props.options &&
    props.options.readOnly &&
    `
    &,
    &:hover {
      --pf-c-form-control--BorderBottomColor: var(--pf-global--BorderColor--300);
    }

    .CodeMirror-cursors {
      display: none;
    }

    .CodeMirror-lines {
      cursor: default;
    }

    .CodeMirror-scroll {
      background-color: var(--pf-c-form-control--disabled--BackgroundColor);
    }
  `}
`;

function CodeMirrorInput({
  value,
  onChange,
  mode,
  readOnly,
  hasErrors,
  rows,
  className,
}) {
  return (
    <CodeMirror
      className={`pf-c-form-control ${className}`}
      value={value}
      onBeforeChange={(editor, data, val) => onChange(val)}
      mode={mode}
      hasErrors={hasErrors}
      options={{
        smartIndent: false,
        lineNumbers: true,
        readOnly,
      }}
      rows={rows}
    />
  );
}
CodeMirrorInput.propTypes = {
  value: string.isRequired,
  onChange: func,
  mode: oneOf(['javascript', 'yaml', 'jinja2']).isRequired,
  readOnly: bool,
  hasErrors: bool,
  rows: number,
};
CodeMirrorInput.defaultProps = {
  readOnly: false,
  onChange: () => {},
  rows: 6,
  hasErrors: false,
};

export default CodeMirrorInput;
