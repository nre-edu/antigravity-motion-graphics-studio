import React from 'react';
import {AbsoluteFill, Audio, Composition, staticFile} from 'remotion';
import {
	FONT_ARABIC_SANS,
	FORMATS,
	GridBackground,
	SelectionBox,
	Sphere3D,
	useEnter,
} from './components/MotionPrimitives';

const StarterScene: React.FC = () => {
	const enter = useEnter(0.1, 0.5);
	return (
		<AbsoluteFill dir="rtl" style={{fontFamily: FONT_ARABIC_SANS}}>
			<GridBackground />
			<Audio src={staticFile('voice.wav')} volume={1} />
			<Audio src={staticFile('sfx.wav')} volume={0.85} />

			<AbsoluteFill
				style={{
					alignItems: 'center',
					justifyContent: 'center',
					padding: `${FORMATS.shorts.safeTop}px ${FORMATS.shorts.safeSide}px ${FORMATS.shorts.safeBottom}px`,
				}}
			>
				<Sphere3D size={110} color1="#bef264" color2="#65a30d" />
				<div
					style={{
						fontSize: 96,
						fontWeight: 900,
						color: '#0f172a',
						lineHeight: 1.4,
						marginTop: 32,
						opacity: enter.opacity,
						filter: `blur(${enter.blur}px)`,
					}}
				>
					عنوان المشهد الرئيسي
				</div>
				<div style={{marginTop: 36}}>
					<SelectionBox borderColor="#1710a8">
						<span style={{fontSize: 48, fontWeight: 800, color: '#1710a8'}}>
							نقطة مفتاحية تفاعلية
						</span>
					</SelectionBox>
				</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

export const Root: React.FC = () => {
	return (
		<Composition
			id="MainVideo"
			component={StarterScene}
			durationInFrames={900}
			fps={30}
			width={FORMATS.shorts.width}
			height={FORMATS.shorts.height}
		/>
	);
};
